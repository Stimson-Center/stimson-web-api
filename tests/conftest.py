import logging

import pytest
import pytest
from flask import Flask
from flask_restful import Api

from scraper.restful.endpoints import create_routes

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@pytest.fixture
def fixture_directory():
    import os
    return os.path.join(os.path.dirname(__file__), "fixtures")


@pytest.fixture(scope='function')
def app():
    app = Flask("test")
    api = Api(app)
    create_routes(api)
    app.logger.setLevel(logging.DEBUG)
    return app
