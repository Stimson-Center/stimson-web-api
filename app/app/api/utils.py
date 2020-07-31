import json
import math
import string
import os
from werkzeug.datastructures import FileStorage


def valid_filename(filename):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    return ''.join(c for c in filename if c in valid_chars)


def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper


def get_google_application_credentials():
    google_application_credentials_file = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    if not google_application_credentials_file:
        raise Exception("GOOGLE_APPLICATION_CREDENTIALS not found")
    try:
        with open(google_application_credentials_file) as f:
            return json.load(f), google_application_credentials_file
    except Exception as ex:
        raise Exception(f"{google_application_credentials_file} not found")


def get_file_storage(fp, filename):
    filestorage =  FileStorage(fp)
    filestorage.filename = filename
    return filestorage
