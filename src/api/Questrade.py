from src.api.ApiDao import ApiDao


def _get_account_call(function, account_id):
    return "{0}/accounts/{1}/{2}".format(Questrade.API_VERSION, account_id, function)


class Questrade(ApiDao):
    API_VERSION = "v1"
    REFRESH_TOKEN_URL = "https://login.questrade.com/oauth2/token?grant_type=refresh_token&refresh_token="
    REFRESH_TOKEN_DURATION = 3 * 24 * 60 * 60

    def __init__(self):  # Constructor
        super().__init__("Questrade", Questrade.REFRESH_TOKEN_URL, Questrade.REFRESH_TOKEN_DURATION)

    def get_time(self):
        endpoint = "{0}/time".format(Questrade.API_VERSION)
        return super().get(endpoint)

    def get_accounts(self):
        endpoint = "{0}/accounts".format(Questrade.API_VERSION)
        return super().get(endpoint)['accounts']

    def get_symbol(self, symbol):
        endpoint = "{0}/symbols/search?prefix={1}".format(Questrade.API_VERSION, symbol)
        return super().get(endpoint)

    def get_positions(self, account_id):
        endpoint = _get_account_call('positions', account_id)
        return super().get(endpoint)['positions']

    def get_order(self, account_id, order_id):
        endpoint = _get_account_call('orders', account_id)+"ids="+order_id
        return super().get(endpoint)["orders"][0]

    def get_balances(self, account_id):
        endpoint = _get_account_call('balances', account_id)
        return super().get(endpoint)

    def get_balance(self, account_id, currency):
        for balance in self.get_balances(account_id)['perCurrencyBalances']:
            if balance['currency'] == currency:
                return balance['cash']

    '''
    def get_markets(self):
        endpoint = "{0}/markets".format(QuestradeDao.API_VERSION)
        return super().get(endpoint)

    def get_quotes(self, id):
        endpoint = "{0}/markets/quotes/{1}".format(QuestradeDao.API_VERSION, id)
        return super().get(endpoint)

    def get_accounts(self):
        endpoint = "{0}/accounts".format(QuestradeDao.API_VERSION)
        return super().get(endpoint)

    def get_activities(self, account_id):
        endpoint = _get_account_call('activities', account_id)
        return super().get(endpoint)    
    '''

    def post_order(self, order):
        endpoint = _get_account_call('orders', order.accountNumber)
        return super().post(endpoint, order.__repr__())["orders"][0]
