import sys

import log4p
import requests
import requests_cache

from src.api.Token import Token

log = log4p.GetLogger(__name__).logger


class Request:

    def __init__(self, name, refresh_token_url, refresh_token_duration):
        self._name = name
        self._token = Token(name, refresh_token_url, refresh_token_duration)
        self.status = None
        self.response = None
        # Caching requests to improve performance and reduce network I/O
        requests_cache.install_cache('api_cache', backend='memory', expire_after=300)

    def get(self, endpoint):
        request_url = self._token.get_api_server() + endpoint
        log.info("GET {0}".format(request_url))
        log.debug("Headers: {0}".format(self._get_headers()))
        response = requests.get(request_url, headers=self._get_headers())

        if response:
            log.info("Request succeeded")
            log.debug("Response: {0} {1}".format(response.status_code, response.json()))
            self.status = response.status_code
            self.response = response.json()
            return response.json()
        else:
            log.error("Request failed - {0} {1} {2}".format(response.status_code, response.reason, response.json()))
            sys.exit()

    def post(self, endpoint, data):
        request_url = self._token.get_api_server() + endpoint
        log.info("GET {0}".format(request_url))
        log.debug("Headers: {0}".format(self._get_headers()))
        response = requests.post(request_url, json=data, headers=self._get_headers())

        if response:
            log.info("Request succeeded")
            log.debug("Response: {0} {1}".format(response.status_code, response.json()))
            return response.json()
        else:
            log.error("Request failed - {0} {1} {2}".format(response.status_code, response.reason, response.json()))
            sys.exit()

    def _get_headers(self):
        token_type = self._token.get_token_type()
        token = self._token.get_access_token()
        auth = "{0} {1}".format(token_type, token)
        return {'Content-Type': 'application/json', "Authorization": auth}
