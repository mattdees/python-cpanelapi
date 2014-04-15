python-cpanelapi
================
This is a simple Python API for cPanel's version 1 (`API1`) and version 2 (`API2`) as well as it's JSON API for WHM.

## Initialization
This API can be used both as a cPanel and WHM users.  In order to use this API with root WHM access, it is recommended to use an access hash.  You can create a client with the following code:

	from cpanelapi import client
	whm = client.Client('root', 'fqdn.server.com', access_hash=access_hash)

You may also create a new cPanel API client by giving a different username, providing a password and setting `cpanel` to True.

	from cpanelapi import client
	cpanel = client.Client('username', 'fqdn.server.com', password=password, cpanel=True)

SSL is enabled by default, but if you do not want to use SSL when sending API requests (not recommended), you can set the `ssl` parameter to False.

## CPanel API v1 Usage
The APIv1 uses ordered parameters.  If you are authenticated to WHM, you are required to provide the `user` parameter in all your calls.  You can leave it out if you're authenticated to cPanel.

    >>> whm.api1('CustInfo', 'getemail', user='username')
	{u'data': {u'result': u'cpanel@customer.com'}, u'module': u'CustInfo', u'source': u'module', u'apiversion': u'1', u'func': u'getemail', u'type': u'event', u'event': {u'result': 1}}

For an example of an API call with parameters:

	>>> whm.api1('Gpg', 'exportsecretkey', 'test', user='username')
	{u'data': {u'result': u''}, u'module': u'Gpg', u'source': u'module', u'apiversion': u'1', u'func': u'exportsecretkey', u'type': u'event', u'event': {u'result': 1}}

For more information, you can reference the [API1 Documentation](http://docs.cpanel.net/twiki/bin/view/ApiDocs/Api1/WebHome).  *Please note that it is recommended to use the API2 calls.*

## CPanel API v2 Usage
The second version of the CPanel API is very similar to the first, with the exception that it uses named parameters instead of ordered ones.  Sample usage:

	>>> whm.api2('Contactus', 'isenabled', user='username')
	{u'cpanelresult': {u'module': u'Contactus', u'func': u'isenabled', u'data': [{u'enabled': 1}], u'event': {u'result': 1}, u'apiversion': 2}}

For an example of an API call with parameters:

	>>> whm.api2('DnsLookup', 'name2ip', user='username', domain='google.com')
	{u'cpanelresult': {u'apiversion': 2, u'module': u'DnsLookup', u'data': [{u'status': 1, u'ip': u'74.125.228.227', u'domain': u'google.com', u'statusmsg': u'Resolved'}], u'event': {u'result': 1}, u'func': u'name2ip'}}

For more information, you can reference the [API2 Documentation](http://docs.cpanel.net/twiki/bin/view/ApiDocs/Api2/WebHome)

## WHM JSON-RPC API Usage
The WHM API is very straightforward and easy to use.  It uses named parameters so you can add those easily.

	>>> whm.call('listaccts')
	{u'status': 1, u'acct': [..snip..], u'statusmsg': u'Ok'}

For an example of an API call with parameters:

	>>> whm.call('accountsummary', user='username')
	{u'status': 1, u'acct': [..snip..], u'statusmsg': u'Ok'}

You can also use the less documented V1 API of the JSON-RPC which seperates the response into two parts: metadata & data.  For example:

	>>> whm.call_v1('listaccts')
	{u'data': {u'acct': [..snip..]}, u'metadata': {u'reason': u'OK', u'version': 1, u'command': u'listaccts', u'result': 1}}

For more information, you can reference the [XML and JSON APIs Documentation](http://docs.cpanel.net/twiki/bin/view/SoftwareDevelopmentKit/XmlApi)

## License
Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.