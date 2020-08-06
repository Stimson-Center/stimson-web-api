
Logger = None


def get_logger():
    global Logger
    return Logger


def set_logger(flask_app, level):
    global Logger
    flask_app.logger.setLevel(level)
    Logger = flask_app.logger
