# https://preslav.me/2019/01/09/dotenv-files-python/
from flask import request
from flask_restful import Resource

# https://preslav.me/2019/01/09/dotenv-files-python/
# noinspection PyPackageRequirements
from scraper import Article
# noinspection PyPackageRequirements
from scraper.configuration import Configuration

__title__ = 'stimson-web-api'
__author__ = 'Alan S. Cooper'
__license__ = 'MIT'
__copyright__ = 'Copyright 2020, The Stimson Center'
__maintainer__ = "The Stimson Center"
__maintainer_email = "cooper@pobox.com"


class ArticleProcess(Resource):
    @staticmethod
    def get():
        # print("Args=" + json.dumps(request.args))
        # print("Values=" + json.dumps(request.values))
        # print("Form=" + json.dumps(request.form))
        url = request.args.get('url')
        language = request.args.get('language')
        language = language[:2]
        article = ArticleProcess.create_article(url, language)
        return article.get_json(), 200, {'Content-Type': 'application/json'}

    @staticmethod
    def create_article(url, language):
        config = Configuration()
        # initialization runtime configuration
        config.follow_meta_refresh = True
        config.use_meta_language = False
        config.set_language(language)
        config.http_success_only = False
        config.ignored_content_types_defaults = {
            # "application/pdf": "%PDF-",
            # "application/x-pdf": "%PDF-",
            "application/x-bzpdf": "%PDF-",
            "application/x-gzpdf": "%PDF-"
        }
        return Article(url, config=config)





