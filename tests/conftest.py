import logging
import pytest
from flask import Flask
from app.app.app import set_cors, set_api

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@pytest.fixture
def fixture_directory():
    import os
    return os.path.join(os.path.dirname(__file__), "fixtures")


@pytest.fixture(scope='function')
def app():
    app = Flask(__name__)
    set_cors(app)
    set_api(app)
    return app
