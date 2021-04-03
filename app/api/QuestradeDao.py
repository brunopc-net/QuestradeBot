from app.api.ApiDao import ApiDao


class QuestradeDao(ApiDao):
    API_VERSION = "v1"
    REFRESH_TOKEN_URL = "https://login.questrade.com/oauth2/token?grant_type=refresh_token&refresh_token="
    REFRESH_TOKEN_DURATION = 3 * 24 * 60 * 60

    def __init__(self):  # Constructor
        super().__init__("Questrade", QuestradeDao.REFRESH_TOKEN_URL, QuestradeDao.REFRESH_TOKEN_DURATION)

    def get_time(self):
        endpoint = "{0}/time".format(QuestradeDao.API_VERSION)
        return super().api_get(endpoint)

    def get_markets(self):
        endpoint = "{0}/markets".format(QuestradeDao.API_VERSION)
        return super().api_get(endpoint)

    def get_quotes(self, id):
        endpoint = "{0}/markets/quotes/{1}".format(QuestradeDao.API_VERSION, id)
        return super().api_get(endpoint)

    def get_symbol(self, symbol):
        endpoint = "{0}/symbols/search?prefix={1}".format(QuestradeDao.API_VERSION, symbol)
        return super().api_get(endpoint)

    def get_accounts(self):
        endpoint = "{0}/accounts".format(QuestradeDao.API_VERSION)
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
        return "{0}/accounts/{1}/{2}".format(QuestradeDao.API_VERSION, account_id, function)
