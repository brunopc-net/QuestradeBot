import log4p
import redis
import json
import requests
import sys

from datetime import datetime
from datetime import timedelta

log = log4p.GetLogger(__name__).logger
redis = redis.Redis()

class TokenStorage:
    
    @staticmethod
    def load(name):
        log.info("Loading token…")
        data = redis.get(name)
        if data is None:
            return data
        return json.loads(data)
    
    @staticmethod
    def store(name, token):
        log.info("Storing token…")
        data = json.dumps(token)
        redis.set(name, data)
        log.info("Storing token: done")
    
    @staticmethod
    def is_stored(name):
        return redis.exists(name)

class Token:
    
    def __init__(self, name, refresh_token_url, refresh_token_duration=0): #Constructor
        log.info("Initiating token {0}".format(name))
        self._name = name
        self._refresh_token_url = refresh_token_url
        self._refresh_token_duration = refresh_token_duration
        self._load()
    
    def _load(self):
        self._registration = TokenStorage.load(self._name)
        if not self._is_registered() or self._is_refresh_expired():
            log.info("Token must be registered")
            self._register()
        elif self._is_expired():
            log.info("Token is expired")
            self._refresh()
    
    def _register(self):
        log.info("Registering token…")
        new_token = self._get_manual_token()
        new_registration = self._request_registration(new_token)
        self._set_registration(new_registration)
        log.info("Registering token: done")
    
    def _refresh(self):
        log.info("Refreshing token…")
        new_token = self.get_refresh_token()
        new_registration = self._request_registration(new_token)
        self._set_registration(new_registration)
        log.info("Refreshing token: done")
    
    def _request_registration(self, token):
        log.info("Requesting new registration…")
        response = requests.get(self._refresh_token_url + token)
        if not response:
            log.error("Request failed, status code: {0}".format(response.status_code))
            log.debug("Request URL: {0}".format(self._refresh_token_url))
            log.debug("Token: {0}".format(token))
            log.fatal("Can't get token registration, terminating ")
            sys.exit()
        return response.json()
    
    def _set_registration(self, new_registration):
        log.debug("New registration returned: {0}".format(new_registration))
        self._registration = new_registration
        log.info("Getting new registration: done")
        self._registration.update({"timestamp": datetime.now().isoformat()})
        TokenStorage.store(self._name, self._registration)
        
    def _is_refresh_expired(self):
        is_refresh_expired = datetime.now() >= self.get_refresh_expiration()
        log.info("Token refresh is expired: {0}".format(is_refresh_expired))
        return is_refresh_expired
    
    def _is_expired(self):
        is_expired = datetime.now() >= self.get_token_expiration()
        log.info("Token is expired: {0}".format(is_expired))
        return is_expired
    
    def _is_registered(self):
        is_registered = self._registration is not None
        log.info("Token is registered: {0}".format(is_registered))
        return is_registered
    
    def get_access_token(self):
        return self._api_name
        
    def get_access_token(self):
        return self._registration['access_token']
    
    def get_token_type(self):
        return self._registration['token_type']
    
    def get_refresh_token(self):
        return self._registration['refresh_token']
    
    def get_api_server(self):
        return self._registration['api_server']
    
    def get_timestamp(self):
        return self._registration['timestamp']
    
    def get_token_expiration(self):
        timestamp = datetime.fromisoformat(self.get_timestamp())
        duration = timedelta(0, seconds=self._registration['expires_in'])
        token_expiration = timestamp + duration
        log.debug("Token expiration: {0}".format(token_expiration))
        return token_expiration
        
    def get_refresh_expiration(self):
        timestamp = datetime.fromisoformat(self.get_timestamp())
        duration = timedelta(0, seconds=self._refresh_token_duration)
        refresh_expiration = timestamp + duration
        log.debug("Token refresh expiration: {0}".format(refresh_expiration))
        return refresh_expiration
    
    @staticmethod
    def _get_manual_token():
        while True:
            manual_token = input("Enter the manually generated token: ").strip()
            if len(manual_token) < 24: #general test.
                print("The token is not valid, please try again")
            else:
                return manual_token