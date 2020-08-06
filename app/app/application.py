import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_restful import Resource

from .api.logger import set_logger
from .api.routes import set_api, set_cors

__title__ = 'stimson-web-api'
__author__ = 'Alan S. Cooper'
__license__ = 'MIT'
__copyright__ = 'Copyright 2020, The Stimson Center'
__maintainer__ = "The Stimson Center"
__maintainer_email = "cooper@pobox.com"

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)
Logger = app.logger


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


set_logger(app, logging.INFO)
set_cors(app)
set_api(app)

print("APP_SETUP")
if __name__ == "__main__":
    # Only for debugging while developing
    handler = RotatingFileHandler('sl-linkedin-api.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.logger.info("IN __main__")
    app.run(host="0.0.0.0", debug=True, port=5000)
