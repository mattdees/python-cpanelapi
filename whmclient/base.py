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


class Resource(object):
    """ Base resource """
    def __init__(self, manager, info, loaded=False):
        self.manager = manager
        self._load_info(info)
        self.loaded = False

    def get(self):
        raise NotImplementedError()

    def __getattr__(self, k):
        if k not in self.__dict__:
            if not self.loaded:
                self.get()
                return self.__getattr__(k)
            raise AttributeError(k)
        else:
            return self.__dict__[k]

    def _load_info(self, info):
        self._info = info
        for k, v in info.iteritems():
            setattr(self, k, v)


class Manager(object):
    """ Base manager """

    def __init__(self, client):
        self.client = client

    def _list(self, url, root=None, loaded=True):
        """ Get the content at URL and generate a list of `resource_class` """
        json = self.client.get(url)

        # Get the root for JSON data
        if root:
            json = json[root]

        return [self.resource_class(self, i, loaded) for i in json]