import log4p
import requests
import requests_cache

from Token import Token

log = log4p.GetLogger(__name__).logger

class ApiDao:
    
    def __init__(self, name, refresh_token_url, refresh_token_duration):
        self._name = name
        self._token = Token(name, refresh_token_url, refresh_token_duration)
        #Caching requests to improve performance and reduce network I/O
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
        token = self._token.get_access_token()
        auth = "{0} {1}".format(token_type, token)
        return {'Content-Type': 'application/json', "Authorization": auth}

class Questrade(ApiDao):
    
    API_VERSION = "v1"
    REFRESH_TOKEN_URL = "https://login.questrade.com/oauth2/token?grant_type=refresh_token&refresh_token="
    REFRESH_TOKEN_DURATION=3*24*60*60
    
    def __init__(self): #Constructor
        super().__init__("Questrade", Questrade.REFRESH_TOKEN_URL, Questrade.REFRESH_TOKEN_DURATION)

    def get_time(self):
        endpoint = "{0}/time".format(Questrade.API_VERSION)
        return super().api_get(endpoint)
    
    def get_markets(self):
        endpoint = "{0}/markets".format(Questrade.API_VERSION)
        return super().api_get(endpoint)
    
    def get_quotes(self, id):
        endpoint = "{0}/markets/quotes/{1}".format(Questrade.API_VERSION, id)
        return super().api_get(endpoint)
    
    def get_symbol(self, symbol):
        endpoint = "{0}/symbols/search?prefix={1}".format(Questrade.API_VERSION, symbol)
        return super().api_get(endpoint)
    
    def get_accounts(self):
        endpoint = "{0}/accounts".format(Questrade.API_VERSION)
        return super().api_get(endpoint)
    
    def get_positions(self, account_id):
        endpoint = self._get_account_call('positions', account_id)
        return super().api_get(endpoint)

    def get_activities(self, account_id):
        endpoint = self._get_account_call('activities', account_id)
        return super().api_get(endpoint)
    
    def get_orders(self, account_id):
        endpoint = self._get_account_call('orders', account_id)
        return super().api_get(endpoint)
    
    def get_balances(self, account_id):
        endpoint = self._get_account_call('balances', account_id)
        return super().api_get(endpoint)
    
    def _get_account_call(self, function, account_id):
        return "{0}/accounts/{1}/{2}".format(Questrade.API_VERSION, account_id, function)