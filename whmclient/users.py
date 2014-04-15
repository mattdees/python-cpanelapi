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

from whmclient import base
from whmclient import exceptions


class User(base.Resource):
    def __repr__(self):
        return '<User: %s>' % self.user

    def get(self):
        """
        This API function will generate a list of an account's attributes,
        such as its IP address and partition.

        Implements:
        - accountsummary
        """
        user = self.manager.get(self.user)
        self._load_info(user._info)

    def set_password(self, password, update_database=False):
        self.manager.client.get('passwd', {'user': self.user, 'pass': password,
                                           'db_pass_update': update_database})



class UserManager(base.Manager):
    resource_class = User

    def get(self, username):
        json = self.client.get('accountsummary', {'user': username})
        return self.resource_class(self, json['acct'][0], loaded=True)

    def list(self, suspended=False, locked=False):
        """
        This API function will generate a list of accounts.

        Implements:
        - listaccts
        - listsuspended
        - listlockedaccounts
        """
        url = 'listaccts'

        if suspended and locked:
            raise exceptions.InvalidParametersException()
        elif suspended:
            return self._list('listsuspended', root='accts', loaded=False)
        elif locked:
            return self._list('listlockedaccounts', root='accts', loaded=False)
        return self._list('listaccts', root='acct')