import json
import sys
import log4p
import configparser
import os

from src.api.QuestradeDao import QuestradeDao
from src.model.AccountType import AccountType
from src.model.Portfolio import Portfolio

log = log4p.GetLogger(__name__).logger
config = configparser.ConfigParser()

questrade = QuestradeDao()


def build_portfolio(account_id):
    balances = questrade.get_balances(account_id)
    positions = questrade.get_positions(account_id)
    return Portfolio(account_id, balances, positions)


def validate_config():
    for account_type in config.sections():
        validate_account_type(account_type)
        validate_account_id(account_type)
        validate_targets(account_type)


def validate_account_id(account_type):
    account_id = "None"
    try:
        account_id = os.environ[get_account_id_field(account_type)]
        if int(account_id) > 99999999 or int(account_id) < 10000000:
            raise ValueError("Questrade account id must be a 8 digits number")
        log.info(get_account_id_field(account_type) + " is correctly set")
    except Exception as e:
        log.fatal(get_account_id_field(account_type) + " env variable is incorrect - value: (" + account_id + ")")
        log.fatal(e)
        sys.exit()


def get_account_id_field(account_type):
    return account_type + '_ACCOUNT_ID'


def validate_targets(account_type):
    total_weight = 0
    tickers = ""
    for ticker, weight in config[account_type].items():
        validate_weight(weight)
        validate_ticker(ticker)
        tickers += ticker.upper() + ","
        total_weight += float(weight)
    validate_total_weight(total_weight, account_type)


def validate_account_type(account):
    if account.upper() in AccountType.__members__:
        log.info("Account: " + account + " will be managed")
    else:
        log.fatal("Account type " + account + " is not a valid account type")
        sys.exit()


def validate_weight(weight):
    try:
        if float(weight) < 0:
            raise ValueError("Sorry, no numbers below zero")
        log.info("Value " + weight + " OK")
    except ValueError:
        log.fatal("Weight value is not valid (" + str(weight) + ")")
        sys.exit()


def validate_ticker(ticker):
    symbol = questrade.get_symbol(ticker)
    response_symbol_ticker = json.loads(symbol).symbols[0].symbol
    log.info(response_symbol_ticker + " is a valid ticker")


def validate_total_weight(total_weight, account_type):
    if total_weight != 1:
        log.error("Total weight your " + account_type + " portfolio: " + str(total_weight))
        log.fatal("Total weight doesn't equal 100%. Please review your tickers/weight and get me back.")
        sys.exit()


def run():
    config.read('../config.ini')
    validate_config()

run()