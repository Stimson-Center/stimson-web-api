# https://preslav.me/2019/01/09/dotenv-files-python/
from textwrap import wrap

from flask import request
from flask_restful import Resource
from google.cloud import translate

# https://preslav.me/2019/01/09/dotenv-files-python/
from scraper.article import TRANSLATED

# noinspection PyPackageRequirements
from .article_process import ArticleProcess
from .utils import get_google_application_credentials

__title__ = 'stimson-web-api'
__author__ = 'Alan S. Cooper'
__license__ = 'MIT'
__copyright__ = 'Copyright 2020, The Stimson Center'
__maintainer__ = "The Stimson Center"
__maintainer_email = "cooper@pobox.com"


class ArticleTranslateException(Exception):
    pass


class ArticleTranslate(Resource):
    @staticmethod
    def post():
        form = request.get_json()
        article = ArticleProcess.create_article(form['url'], form['config']['language'])
        article.set_json(form)
        article.throw_if_not_downloaded_verbose()
        article.throw_if_not_parsed_verbose()
        if article.config.get_language == "en":
            raise ArticleTranslateException("Article Configuration language is already 'en'")
        target_language = "en"
        client = translate.TranslationServiceClient()
        google_application_credentials, google_application_credentials_file = get_google_application_credentials()
        if 'project_id' not in google_application_credentials:
            raise ArticleTranslateException(f"project_if not found in {google_application_credentials_file}")
        parent = client.location_path(google_application_credentials['project_id'], "global")
        title = ArticleTranslate.google_translate_text(client, parent, article.title, article.config.language,
                                                       target_language)
        text = ArticleTranslate.google_translate_text(client, parent, article.text, article.config.language,
                                                      target_language)
        # set the langage, STOP_WORDS for the Natural Language Processing
        article.config.set_language(target_language)
        article.set_title(title)
        article.set_text(text)
        article.nlp()
        article.set_workflow(TRANSLATED)
        return article.get_json(), 200, {'Content-Type': 'application/json'}

    @staticmethod
    def google_translate_text(client, parent, source_text, source_language, target_language):
        target_text = ''
        if source_text and len(source_text):
            # Detail on supported types can be found here:
            # https://cloud.google.com/translate/docs/supported-formats
            # GOOGLE error: 'Request payload size exceeds the limit: 204800 bytes.'
            # Cooper: TODO: NOTE: 50000 give error Input too long!
            for source_text_block in wrap(source_text, 10000):
                response = client.translate_text(
                    parent=parent,
                    contents=[source_text_block],
                    mime_type="text/plain",  # mime types: text/plain, text/html
                    source_language_code=source_language,
                    target_language_code=target_language,
                )
                # Display the translation for each input text provided
                for translation in response.translations:
                    target_text += translation.translated_text
        return target_text

