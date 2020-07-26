from flask import Flask
import logging
from flask_cors import CORS
from flask_restful import Api
from flask_restful import Resource

from .api.article_process import ArticleProcess
from .api.countries import Countries
from .api.file_types import FileTypes
from .api.health import Health
from .api.languages import Languages
from .api.pdf import PDF
from .api.search import Search
from .api.share import Share
from .api.article_translate import ArticleTranslate

__title__ = 'stimson-web-api'
__author__ = 'Alan S. Cooper'
__license__ = 'MIT'
__copyright__ = 'Copyright 2020, The Stimson Center'
__maintainer__ = "The Stimson Center"
__maintainer_email = "cooper@pobox.com"

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)
Logger = app.logger

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


def set_cors(flask_app):
    # https://github.com/corydolphin/flask-cors/issues/201
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Headers
    CORS(flask_app,
         resources={r"/*": {"origins": "*"}},
         # origins=f"http://127.0.0.1:{port}",
         allow_headers=[
             "Access-Control-Allow-Credentials",
             "Access-Control-Allow-Headers",
             "Access-Control-Allow-Methods",
             "Access-Control-Allow-Origin",
             "Authorization",
             "Content-Type",
         ],
         supports_credentials=True
         )

def set_api(flask_app):
    api = Api(flask_app)
    api.add_resource(Health, '/')
    api.add_resource(ArticleProcess, '/article')
    api.add_resource(ArticleTranslate, '/article/translate')
    api.add_resource(Countries, '/countries')
    api.add_resource(FileTypes, '/filetypes')
    api.add_resource(Languages, '/languages')
    api.add_resource(PDF, '/pdf')
    api.add_resource(Search, '/search')
    api.add_resource(Share, '/share')

# @app.before_request
# def authorize_token():
#     pass
#     # if request.endpoint != 'token':
#     #     try:
#     #         auth_header = request.headers.get("Authorization")
#     #         if "Bearer" in auth_header:
#     #             token = auth_header.split(' ')[1]
#     #             if token != '12345678':
#     #                 raise ValueError('Authorization failed.')
#     #     except Exception as e:
#     #         return "401 Unauthorized\n{}\n\n".format(e), 401


class GetToken(Resource):
    @staticmethod
    def post():
        token = '12345678'
        return token  # token sent to client to return in subsequent
        # requests in Authorization header


set_cors(app)
set_api(app)

print("APP_SETUP")
if __name__ == "__main__":
    # Only for debugging while developing
    app.logger.info("IN MAIN")
    app.run(host="0.0.0.0", debug=True, port=5000)
