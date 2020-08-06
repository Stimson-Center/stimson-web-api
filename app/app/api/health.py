import json
import shutil

import psutil
import scraper
from flask_restful import Resource

from .logger import get_logger
from .version import __version__


class Health(Resource):
    @staticmethod
    def get():
        logger = get_logger()
        total, used, free = shutil.disk_usage("/")
        response = {
            'cpu_in_use': psutil.cpu_percent(),
            'memory_in_use': psutil.virtual_memory().percent,
            'diskspace_in_use': round(used / total * 100, 1),
            'scraper_version': scraper.__version__,
            'api_version': __version__
        }
        logger.info(json.dumps(response))
        return response, 200, {'Content-Type': 'application/json'}
