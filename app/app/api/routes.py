from flask_cors import CORS
from flask_restful import Api

from .article_download import ArticleDownload
from .article_nlp import ArticleNLP
from .article_parse import ArticleParse
from .article_process import ArticleProcess
from .article_translate import ArticleTranslate
from .countries import Countries
from .file_types import FileTypes
from .google_drive import GoogleDrive
from .google_storage import GoogleStorage
from .health import Health
from .languages import Languages
from .pdf import PDF
from .search import Search


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
    api.add_resource(ArticleDownload, '/article/download')
    api.add_resource(ArticleParse, '/article/parse')
    api.add_resource(ArticleNLP, '/article/nlp')
    api.add_resource(ArticleTranslate, '/article/translate')
    api.add_resource(Countries, '/countries')
    api.add_resource(GoogleDrive, "/drive")
    api.add_resource(FileTypes, '/filetypes')
    api.add_resource(GoogleStorage, "/store")
    api.add_resource(Languages, '/languages')
    api.add_resource(PDF, '/pdf')
    api.add_resource(Search, '/search')
