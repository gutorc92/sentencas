# -*- coding: utf-8 -*-
import os
import json
import codecs
from model.models import create_process

import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from settings import Settings
from apiclient.http import MediaFileUpload

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive.file'
CLIENT_SECRET_FILE = 'client_secret_664606804106-lkbr670fg3reem4310k3g2hp4dnjpaal.apps.googleusercontent.com.json'
APPLICATION_NAME = 'Teste sentencas'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.dirname(os.path.abspath(__file__))
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def upload_file(dir_file, file_name):
    dir_ = os.path.dirname(os.path.abspath(__file__))
    folder_id = '19kJF67QmUwh6DP4Z0rBaDGyfm6OBSitC'
    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    media = MediaFileUpload(os.path.join(dir_file, file_name),
                            mimetype='text/json',
                            resumable=True)
    file = service.files().create(body=file_metadata,
                                        media_body=media, fields='id').execute()

    print('File ID: %s' % file.get('id'))

def main():
    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    for up to 10 files.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    results = service.files().list(q="mimeType = 'application/vnd.google-apps.folder' and name = 'files'", fields="nextPageToken, files(id, name)").execute()
    print(results)
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id']))


if __name__ == '__main__':
    dir_ = os.path.dirname(os.path.abspath(__file__))
    upload_file(dir_, "varas.txt")
