# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Demonstrates how to authenticate to Google Cloud Platform APIs using
the Google Cloud Client Libraries."""

import json
import os

from dotenv import load_dotenv
from flask import request
from flask_restful import Resource
from google.auth import compute_engine
from google.cloud import storage
from googleapiclient import discovery

__title__ = 'stimson-web-api'
__author__ = 'Alan S. Cooper'
__license__ = 'MIT'
__copyright__ = 'Copyright 2020, The Stimson Center'
__maintainer__ = "The Stimson Center"
__maintainer_email = "cooper@pobox.com"


class GoogleStorage(Resource):
    @staticmethod
    def post():
        """Process the uploaded file and upload it to Google Cloud Storage."""
        uploaded_file = request.files.get('file')

        if not uploaded_file:
            return 'No file uploaded.', 400

        # Create a Cloud Storage client.
        gcs = storage.Client()

        # Get the bucket that the file will be uploaded to.
        # https://codelabs.developers.google.com/codelabs/gsuite-apis-intro/#0
        # Alternative way to write files to Google Cloud:
        #   https://cloud.google.com/appengine/docs/standard/python/googlecloudstorageclient/app-engine-cloud-storage-sample
        # Get environment variables
        load_dotenv()
        gcs_storage_bucket = os.getenv('GCS_STORAGE_BUCKET')
        bucket = gcs.get_bucket(gcs_storage_bucket)

        # Create a new blob and upload the file's content.
        blob = bucket.blob(uploaded_file.filename)

        blob.upload_from_string(
            uploaded_file.read(),
            content_type=uploaded_file.content_type
        )

        # The public URL can be used to directly access the uploaded file via HTTP.
        return blob.public_url, 200, {'Content-Type': 'application/json'}


def implicit():
    # If you don't specify credentials when constructing the client, the
    # client library will look for credentials in the environment.
    storage_client = storage.Client()
    return storage_client


def explicit():
    # Explicitly use service account credentials by specifying the private key
    # file.
    storage_client = storage.Client.from_service_account_json('service_account.json')
    return storage_client


def explicit_compute_engine(project):
    # Explicitly use Compute Engine credentials. These credentials are
    # available on Compute Engine, App Engine Flexible, and Container Engine.
    credentials = compute_engine.Credentials()

    # Create the client using the credentials and specifying a project ID.
    storage_client = storage.Client(credentials=credentials, project=project)
    return storage_client


def create_storage_service():
    """Creates the service object for calling the Cloud Storage API."""
    # Construct the service object for interacting with the Cloud Storage API -
    # the 'storage' service, at version 'v1'.
    # You can browse other available api services and versions here:
    #     https://developers.google.com/api-client-library/python/apis/
    return discovery.build('storage', 'v1')


def get_bucket_metadata(bucket):
    """Retrieves metadata about the given bucket."""
    service = create_storage_service()

    # Make a request to buckets.get to retrieve a list of objects in the
    # specified bucket.
    req = service.buckets().get(bucket=bucket)
    return req.execute()


def list_bucket(bucket):
    """Returns a list of metadata of the objects within the given bucket."""
    service = create_storage_service()

    # Create a request to objects.list to retrieve a list of objects.
    fields_to_return = \
        'nextPageToken,items(name,size,contentType,metadata(my-key))'
    req = service.objects().list(bucket=bucket, fields=fields_to_return)

    all_objects = []
    # If you have too many items to list in one request, list_next() will
    # automatically handle paging with the pageToken.
    while req:
        resp = req.execute()
        all_objects.extend(resp.get('items', []))
        req = service.objects().list_next(req, resp)
    return all_objects


def upload_to_bucket(bucket, destination, sources):
    # Construct the service object for the interacting with the Cloud Storage
    # API.
    service = discovery.build('storage', 'v1')

    # Upload the source files.
    for filename in sources:
        req = service.objects().insert(
            media_body=filename,
            name=filename,
            bucket=bucket)
        resp = req.execute()
        print('> Uploaded source file {}'.format(filename))
        print(json.dumps(resp, indent=2))

    # Construct a request to compose the source files into the destination.
    compose_req_body = {
        'sourceObjects': [{'name': filename} for filename in sources],
        'destination': {
            'contentType': 'text/plain',  # required
        }
    }

    req = service.objects().compose(
        destinationBucket=bucket,
        destinationObject=destination,
        body=compose_req_body)

    resp = req.execute()

    print('> Composed files into {}'.format(destination))
    print(json.dumps(resp, indent=2))

    # Download and print the composed object.
    req = service.objects().get_media(
        bucket=bucket,
        object=destination)

    res = req.execute()

    print('> Composed file contents:')
    print(res)
