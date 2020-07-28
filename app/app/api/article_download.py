# https://preslav.me/2019/01/09/dotenv-files-python/

from flask import request
from flask_restful import Resource

# noinspection PyPackageRequirements
from .article_process import ArticleProcess

# https://preslav.me/2019/01/09/dotenv-files-python/

__title__ = 'stimson-web-api'
__author__ = 'Alan S. Cooper'
__license__ = 'MIT'
__copyright__ = 'Copyright 2020, The Stimson Center'
__maintainer__ = "The Stimson Center"
__maintainer_email = "cooper@pobox.com"


class ArticleDownload(Resource):
    @staticmethod
    def post():
        form = request.get_json()
        article = ArticleProcess.create_article(form['url'], form['config']['language'])
        article.set_json(form)
        article.download()
        return article.get_json(), 200, {'Content-Type': 'application/json'}
