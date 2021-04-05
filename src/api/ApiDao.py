import log4p
import requests
import requests_cache

from Token import Token

log = log4p.GetLogger(__name__).logger

class ApiDao:

    def __init__(self, name, refresh_token_url, refresh_token_duration):
        self._name = name
        self._token = Token(name, refresh_token_url, refresh_token_duration)
        # Caching requests to improve performance and reduce network I/O
        requests_cache.install_cache('api_cache', backend='memory', expire_after=300)

    def api_get(self, endpoint):
        request_url = self._token.get_api_server() + endpoint
        log.info("GET request for {0}".format(request_url))
        response = requests.get(request_url, headers=self._get_headers())

        if response:
            log.info("Request succeeded")
        else:
            log.error("Request failed: {0}".format(response.status_code))

        return response.json()

    def get_name(self):
        return self._name

    def _get_headers(self):
        token_type = self._token.get_token_type()
        token = self._token.get_token()
        auth = "{0} {1}".format(token_type, token)
        return {'Content-Type': 'application/json', "Authorization": auth}
