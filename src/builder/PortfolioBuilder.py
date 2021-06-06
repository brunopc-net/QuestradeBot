import log4p

from src import Config
from src.api.QuestradeDao import QuestradeDao
from src.model.Portfolio import Portfolio

log = log4p.GetLogger(__name__, config="../log4p.json").logger
Questrade = QuestradeDao()


def build(account_type):
    account_id = str(Config.get_account_id(account_type))
    balance = __get_account_balance(account_id, 'CAD')
    positions = __get_positions(account_id)
    portfolio = Portfolio(account_type, account_id, positions, balance)
    log.info("Portfolio loaded: " + account_type + " " + str(portfolio))
    return portfolio


def __get_account_balance(account_id, currency):
    for balance in Questrade.get_balances(account_id)['perCurrencyBalances']:
        if balance['currency'] == currency:
            return balance['cash']


def __get_positions(account_id):
    return Questrade.get_positions(account_id)['positions']
