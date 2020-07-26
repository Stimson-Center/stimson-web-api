import shutil

import psutil
from flask_restful import Resource
import scraper
from .version import __version__


class Health(Resource):
    @staticmethod
    def get():
        total, used, free = shutil.disk_usage("/")
        return {
            'cpu_in_use': psutil.cpu_percent(),
            'memory_in_use': psutil.virtual_memory().percent,
            'diskspace_in_use': round(used / total * 100, 1),
            'scraper_version': scraper.__version__,
            'api_version': __version__
        }
