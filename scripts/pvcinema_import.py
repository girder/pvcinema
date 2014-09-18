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
import json

# TODO(cpatrick): These are hardcoded to my install and need to be fixed
COLLECTION_ID = '541b12e259d2c77b18c99470'
SERVER_ROOT = 'http://localhost:9000/api/v1'
USERNAME = 'cpatrick'
PASSWORD = '2pw4kw'


def login():
    resp = requests.get('{}/user/authentication'.format(SERVER_ROOT),
                        auth=HTTPBasicAuth(USERNAME, PASSWORD))
    return resp.json()['authToken']['token']


def push_folder(input, parent, token):
    params = {'parentType': 'collection',
              'parentId': parent,
              'name': input['title'],
              'description': input['description'],
              'foo': 'bar',
              'public': True}
    headers = {'Girder-Token': token}
    requests.post('{}/folder'.format(SERVER_ROOT),
                  params=params,
                  headers=headers)


def main():

    if len(sys.argv) != 2:
        print('Please specify an input json file.')
        sys.exit(1)

    token = login()

    with open(sys.argv[1], 'r') as infile:
        json_data = json.load(infile)
        for dataset in json_data:
            push_folder(dataset, COLLECTION_ID, token)


if __name__ == '__main__':
    main()
