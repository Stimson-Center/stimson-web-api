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

import os
import os.path
import pickle

from dotenv import load_dotenv
from flask_restful import Resource
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

from .getfilelist import GetFileList, GetFolderTree

DATASCIENCE_FOLDER_ID = '1FwF_u-sLe83I6cjldWJuLgCHkilNse-1'

def get_google_drive_creds():
    # If modifying these scopes, delete the file token.pickle.
    # https://developers.google.com/identity/protocols/oauth2/scopes
    # SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
    SCOPES = ['https://www.googleapis.com/auth/drive']  # C.R.U.D
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    this_file_path = os.path.dirname(os.path.abspath(__file__))
    token_file_path = os.path.abspath(os.path.join(this_file_path, '..', '..', 'token.pickle'))
    if os.path.exists(token_file_path):
        with open(token_file_path, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            load_dotenv()
            google_drive_credentials = os.getenv('GOOGLE_DRIVE_CREDENTIALS')
            flow = InstalledAppFlow.from_client_secrets_file(google_drive_credentials, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds


# https://developers.google.com/drive/api/v3/quickstart/python
def create_drive_service():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    return build('drive', 'v3', credentials=get_google_drive_creds())


def list_drive_folders(folder_id):
    resource = {
        "oauth2": get_google_drive_creds(),
        "id": folder_id,
        "fields": "files(name,id)",
    }
    return GetFolderTree(resource)


def list_drive_folder_files(folder_id):
    resource = {
        "oauth2": get_google_drive_creds(),
        "id": folder_id,
        "fields": "files(name,id)",
    }
    return GetFileList(resource)


# https://developers.google.com/drive/api/v3/manage-uploads#python
class GoogleDrive(Resource):
    @staticmethod
    def post():
        from flask import request

        """Process the uploaded file and upload it to Google Cloud Storage."""
        uploaded_file = request.files.get('file')

        if not uploaded_file:
            return 'No file uploaded.', 400

        # Create a Google Drive client.
        service = create_drive_service()
        metadata = {
            'name': uploaded_file.filename,
            'mimeType': uploaded_file.mimetype,
            'parents': [DATASCIENCE_FOLDER_ID]
        }
        # the file's contents is already in memory with the file pointer pass to this function
        media = MediaIoBaseUpload(uploaded_file,
                                  chunksize=1024 * 1024,
                                  mimetype=uploaded_file.mimetype,
                                  resumable=True
                                  )
        file_id = GoogleDrive.file_exists(uploaded_file.filename)
        if file_id:
            request = service.files().update(body=metadata,
                                             media_body=media,
                                             fileId=file_id
                                             )
        else:
            request = service.files().create(body=metadata,
                                             media_body=media,
                                             fields='id'
        )
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print("Uploaded %d%%." % int(status.progress() * 100))

        # The public URL can be used to directly access the uploaded file via HTTP.
        return response['id'], 200, {'Content-Type': 'application/json'}

    @staticmethod
    def file_exists(filename):
        results = list_drive_folder_files(DATASCIENCE_FOLDER_ID)
        for files in results['fileList']:
            for file in files['files']:
                if file['name'] == filename:
                    return file['id']
        return None


# https://levelup.gitconnected.com/google-drive-api-with-python-part-ii-connect-to-google-drive-and-search-for-file-7138422e0563
def retrieve_all_files():
    service = create_drive_service()
    results = []
    page_token = None
    while True:
        param = {'pageSize': 100, 'fields': "nextPageToken, files(id, name)"}
        if page_token:
            param['pageToken'] = page_token
        files = service.files().list(**param).execute()
        # append the files from the current result page to our list
        results.extend(files.get('files'))
        # Google Drive API shows our files in multiple pages when the number of files exceed 100
        page_token = files.get('nextPageToken')
        if not page_token:
            break
    return results
