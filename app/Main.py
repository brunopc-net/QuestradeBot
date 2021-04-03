import math
import sys
import log4p
import configparser

# from app.PortfolioManager import PortfolioManager
# from app.api.QuestradeDao import QuestradeDao
from app.model.AccountType import AccountType

log = log4p.GetLogger(__name__).logger
config = configparser.ConfigParser()


def run():
    config.read('../config.ini')
    validate_config()


def validate_config():
    for account_type in config.sections():
        validate_account(account_type)
        total_weight = 0
        for ticker, weight in config[account_type].items():
            log.info("Ticker: " + ticker + ", Weight: " + weight)
            validate_weight(weight)
            total_weight += float(weight)
        validate_total_weight(total_weight, account_type)


def validate_account(account):
    if account.upper() in AccountType.__members__:
        log.info("Account: " + account + " will be managed")
    else:
        log.fatal("Account type " + account + " is not a valid account type")
        sys.exit()


def validate_weight(weight):
    try:
        if float(weight) < 0:
            raise ValueError("Sorry, no numbers below zero")
    except ValueError:
        log.fatal("Weight value is not valid (" + str(weight) + ")")
        sys.exit()


def validate_total_weight(total_weight, account_type):
    if total_weight != 1:
        log.error("Total weight your " + account_type + " portfolio: " + str(total_weight))
        log.fatal("Total weight doesn't equal 100%. Please review your tickers/weight and get me back.")
        sys.exit()


run()
