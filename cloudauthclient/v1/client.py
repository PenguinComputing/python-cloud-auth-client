# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2013 Penguin Computing, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#

import logging
from threading import Lock
from datetime import datetime
from httplib import OK as HTTP_OK

import oauth2 as oauth
import simplejson as json

import cloudauthclient.exceptions as exc
from cloudauthclient import client
from cloudauthclient.common.token import Token

LOG = logging.getLogger(__name__)
_TOKEN = None
_TOKEN_LOCK = Lock()


class Client(client.HTTPClient):
    """Client for Scyld Cloud Auth v1 API"""

    def __init__(self, endpoint=None, api_key=None, api_secret=None):
        """Initialize a new client for cloudauth"""
        super(Client, self).__init__(
            endpoint=endpoint,
            api_key=api_key,
            api_secret=api_secret)

    @property
    def token(self):
        return self._get_token()

    def authenticate(self):
        self._get_token()

    def _get_token(self):
        def acquire_token():
            global _TOKEN

            LOG.debug("Requesting new Auth Token")
            url = self.endpoint + "/auth/request_token"
            consumer = oauth.Consumer(
                key=self.api_key,
                secret=self.api_secret)
            client = oauth.Client(consumer)
            try:
                resp, content = client.request(url, "GET")
            except Exception as e:
                LOG.critical(e)
                raise exc.AuthenticationError()
            else:
                if int(resp['status']) != HTTP_OK:
                    LOG.critical("Error returned from CloudAuth: %s",
                                 resp['status'])
                    raise exc.AuthenticationError()
            result = json.loads(content)
            try:
                parsed_time = datetime.strptime(result['expires_at_utc'][:19],
                                                "%Y-%m-%dT%H:%M:%S")
            except ValueError as e:
                LOG.critical(e)
                raise exc.AuthenticationError("Invalid format for Token")
            else:
                LOG.debug("New Token: %s, expires: %s",
                          result['authentication_token'],
                          result['expires_at_utc'])
                _TOKEN = Token(result['authentication_token'], parsed_time)

        with _TOKEN_LOCK:
            # Check if we have an existing access_token to CloudAuth
            if _TOKEN is not None:
                LOG.debug("Found existing token: %s", _TOKEN.token)
                # Is it expired?
                if (datetime.utcnow() >= _TOKEN.expires):
                    LOG.debug("Existing token expired")
                    acquire_token()
            else:
                acquire_token()

        return _TOKEN.token
