# Copyright (c) 2014 VEXXHOST, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import requests
from requests.auth import AuthBase

from whmclient import exceptions
from whmclient.users import UserManager


class AccessHashAuth(AuthBase):
    """ Access hash authentication for requests """

    def __init__(self, access_hash):
        self.access_hash = access_hash.replace('\n', '')

    def __call__(self, r):
        r.headers['Authorization'] = 'WHM root:%s' % self.access_hash
        return r


class Client(object):
    """ Client for WHM JSONAPI """

    def __init__(self, server, access_hash, secure=True):
        self.server = server
        self.auth = AccessHashAuth(access_hash)
        self.secure = secure

        # TODO(mnaser): Load managers more effectively
        self.users = UserManager(self)


    def _generate_url(self, path):
        if self.secure:
            return 'https://%s:2087/json-api/%s' % (self.server, path)
        return 'http://%s:2086/json-api/%s' % (self.server, path)

    def get(self, path, params={}):
        url = self._generate_url(path)
        params.update({'api.version': 1})

        r = requests.get(url, params=params, auth=self.auth)
        json = r.json()
        print json

        if json['metadata']['result'] != 1:
            raise exceptions.ServerError(json['metadata']['reason'])

        return json['data']
