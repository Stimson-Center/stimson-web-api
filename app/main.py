
# app.py - a minimal flask api using flask_restful
# https://medium.com/@doedotdev/docker-flask-a-simple-tutorial-bbcb2f4110b5
# https://github.com/flask-restful/flask-restful/blob/master/examples/todo.py

import logging

from flask_restful import Api

from flask import Flask
from scraper.restful.endpoints import create_routes, set_cors

# from .api.endpoints import create_routes

Logger = None


def create_app(name):
    global Logger

    flask_app = Flask(name)
    flask_app.logger.setLevel(logging.DEBUG)
    Logger = flask_app.logger
    api = Api(flask_app)
    cors = set_cors(flask_app)
    create_routes(api)
    return flask_app


app = create_app("app")


__title__ = 'stimson-web-curator'
__author__ = 'Alan S. Cooper'
__license__ = 'MIT'
__copyright__ = 'Copyright 2020, The Stimson Center'
__maintainer__ = "The Stimson Center"
__maintainer_email = "cooper@pobox.com"

if __name__ == "__main__":
    # Only for debugging while developing
    app.logger.info("IN MAIN")
    app.run(host="0.0.0.0", debug=True, port=5000)
