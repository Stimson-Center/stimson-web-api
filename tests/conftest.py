import logging
import pytest
from app.app.main import app, api

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@pytest.fixture
def fixture_directory():
    import os
    return os.path.join(os.path.dirname(__file__), "fixtures")


@pytest.fixture(scope='function')
def app():
    # api.testing = True
    # client = api.test_client()
    return app
