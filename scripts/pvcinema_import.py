#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#  Copyright Kitware Inc.
#
#  Licensed under the Apache License, Version 2.0 ( the "License" );
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
###############################################################################

# TODO(cpatrick): Currently using requests instead of girder client since
# authentication has changed a bit. This should be changed once girder client
# has moved forward to reflect that.

import requests
from requests.auth import HTTPBasicAuth
import sys
import os
import json
from glob import glob

# TODO(cpatrick): These are hardcoded to my install and need to be fixed
COLLECTION_ID = '541b58df59d2c78586d9fd8f'
SERVER_ROOT = 'http://localhost:9000/api/v1'
STATIC_WEB_DATA_ROOT = 'http://localhost:8080/data'
USERNAME = 'cpatrick'
PASSWORD = '2pw4kw'


def login():
    resp = requests.get('{}/user/authentication'.format(SERVER_ROOT),
                        auth=HTTPBasicAuth(USERNAME, PASSWORD))
    return resp.json()['authToken']['token']


def push_folder(input, parentId, token, directory):
    params = {'parentType': 'collection',
              'parentId': parentId,
              'name': input['title'],
              'description': input['description'],
              'public': True}
    headers = {'Girder-Token': token}
    resp = requests.post('{}/folder'.format(SERVER_ROOT),
                         params=params,
                         headers=headers)
    if resp.status_code != 200:
        return None
    else:
        folder = resp.json()
    print(folder)
    metadata = input
    del metadata['title']
    del metadata['description']
    metadata['pvcinema'] = 1
    metadata['webpath'] = '{}/{}'.format(STATIC_WEB_DATA_ROOT, directory)
    resp = requests.put('{}/folder/{}/metadata'.format(SERVER_ROOT,
                                                       folder['_id']),
                        headers=headers,
                        data=json.dumps(metadata))
    return resp.json()


def push_item(input, folderId, token):
    params = {'folderId': folderId,
              'name': input['title'],
              'input': input['description']}
    headers = {'Girder-Token': token}
    resp = requests.post('{}/item'.format(SERVER_ROOT),
                         params=params,
                         headers=headers)
    item = resp.json()
    metadata = input
    del metadata['title']
    del metadata['description']
    metadata['pvcinema'] = 1
    resp = requests.put('{}/item/{}/metadata'.format(SERVER_ROOT, item['_id']),
                        headers=headers,
                        data=json.dumps(metadata))
    return resp.json()


def main():

    if len(sys.argv) != 2:
        print('Please specify an input folder.')
        sys.exit(1)

    token = login()

    dirs = [f for f in glob('{}/*'.format(sys.argv[1])) if os.path.isdir(f)]
    for directory in dirs:
        json_file = os.path.join(directory, 'info.json')
        if os.path.exists(json_file):
            with open(json_file, 'r') as infile:
                json_data = json.load(infile)
                folder = push_folder(json_data, COLLECTION_ID, token,
                                     os.path.basename(directory))
                if folder:
                    for a in json_data['analysis']:
                        push_item(a, folder['_id'], token)

if __name__ == '__main__':
    main()
