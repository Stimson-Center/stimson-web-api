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
import pytest
import io

from app.app.api.google_drive import list_drive_folder_files, DATASCIENCE_FOLDER_ID

@pytest.mark.options(debug=True)
def test_google_drive_store_file(fixture_directory, client):
    test_driver_file = os.path.join(fixture_directory, "txt", "DO_NOT_DELETE.txt")
    with open(test_driver_file) as fp:
        payload = fp.read()
    # https://stackoverflow.com/questions/35684436/testing-file-uploads-in-flask
    data = dict(
        file=(io.BytesIO(payload.encode()), "DO_NOT_DELETE.txt"),
    )
    response = client.post("/drive", content_type='multipart/form-data', data=data)

    assert 200 == response.status_code
    assert '200 OK' == response.status
    assert 'utf-8' == response.charset
    assert response.data


def test_list_google_drive_files():
    results = list_drive_folder_files(DATASCIENCE_FOLDER_ID)
    for files in results['fileList']:
        for file in files['files']:
            print(f"{file['name']} ({file['id']})")
    # files = retrieve_all_files()
    # for file in files:
    #     print(u'{0} ({1})'.format(file['name'], file['id']))
