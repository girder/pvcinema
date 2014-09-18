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

from girder.api.describe import Description
from girder.api.rest import Resource
from girder.utility.model_importer import ModelImporter


class PVCinema(Resource):
    def __init__(self):
        self.resourceName = 'pvcinema'

        self.route('GET', ('info',), self.makeInfo)

    def makeInfo(self, params):
        """
        Dynamically generate a cinema info file from girder data marked as
        cinema-viewable.
        """

        folderModel = ModelImporter().model('folder')
        folders = folderModel.find({'meta.pvcinema': 1})
        ret = [{'title': f['name'],
                'description': f['description'],
                'path': f['meta']['webpath']} for f in folders]
        return ret
    makeInfo.description = (
        Description('Get a paraview cinema info json blob')
        .notes('The blob will contain the list of datasets available for '
               'viewing in the cinema workbench.'))
