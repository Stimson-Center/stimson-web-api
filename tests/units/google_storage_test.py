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

import os
import mock
import pytest
import io

import google.auth
from dotenv import load_dotenv

from app.app.api.google_storage import implicit, explicit, explicit_compute_engine, list_bucket



@pytest.mark.skip(reason="Running this test updates Google Drive")
def test_google_cloud_store_file(fixture_directory, client):
    test_driver_file = os.path.join(fixture_directory, "txt", "DO_NOT_DELETE.txt")
    with open(test_driver_file) as fp:
        payload = fp.read()
    # https://stackoverflow.com/questions/35684436/testing-file-uploads-in-flask
    data = dict(
        file=(io.BytesIO(payload.encode()), "DO_NOT_DELETE.txt"),
    )
    response = client.post("/store", content_type='multipart/form-data', data=data)

    assert 200 == response.status_code
    assert '200 OK' == response.status
    assert 'utf-8' == response.charset
    assert response.data


def test_implicit():
    storage_client = implicit()
    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    assert (len(buckets))
    print(buckets)


def test_explicit():
    with open(os.environ['GOOGLE_APPLICATION_CREDENTIALS']) as creds_file:
        creds_file_data = creds_file.read()

    open_mock = mock.mock_open(read_data=creds_file_data)

    with mock.patch('io.open', open_mock):
        storage_client = explicit()

        # Make an authenticated API request
        buckets = list(storage_client.list_buckets())
        assert (len(buckets))
        print(buckets)


def test_explicit_compute_engine():
    adc, project = google.auth.default()
    credentials_patch = mock.patch(
        'google.auth.compute_engine.Credentials', return_value=adc)

    with credentials_patch:
        storage_client = explicit_compute_engine(project)
        # Make an authenticated API request
        buckets = list(storage_client.list_buckets())
        print(buckets)


def test_list_google_storage_bucket_files():
    # Get environment variables
    load_dotenv()
    gcs_storage_bucket = os.getenv('GCS_STORAGE_BUCKET')
    files = list_bucket(gcs_storage_bucket)
    # output the file metadata to console
    for file in files:
        print(file)
