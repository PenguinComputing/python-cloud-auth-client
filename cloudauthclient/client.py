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

import requests

import exceptions as exc

LOG = logging.getLogger(__name__)


class HTTPClient(object):
    """Client to handle HTTP traffic to cloudauth"""

    USER_AGENT = "python-cloud-auth-client"

    def __init__(self, endpoint=None, api_key=None, api_secret=None):
        self.endpoint = endpoint
        self.api_key = api_key
        self.api_secret = api_secret

        if self.endpoint is None:
            raise(exc.NoEndpointError("No endpoint given for CloudAuth"))

        self.http = requests.Session()

    def request(self, url, method, **kwargs):
        resp = self.http.request(
            method,
            url,
            **kwargs)

        return resp
