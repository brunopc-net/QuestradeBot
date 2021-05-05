import sys
import log4p
import configparser
import os

from api.QuestradeDao import QuestradeDao
from model.AccountType import AccountType

log = log4p.GetLogger(__name__, config="../log4p.json").logger
config = configparser.ConfigParser()

questrade = QuestradeDao()


def validate_config():
    for account_type in get_account_types():
        validate_account_type(account_type)
        validate_account_id(account_type)
        validate_targets(account_type)


def validate_account_id(account_type):
    log.info("Validating account id " + account_type)
    try:
        account_id = get_account_id(account_type)
        if int(account_id) > 99999999 or int(account_id) < 10000000:
            raise ValueError("Questrade account id must be a 8 digits number")
        log.info(get_account_id_field(account_type) + " is correctly set")
    except Exception as e:
        log.fatal(get_account_id_field(account_type) + " env variable is incorrect - value: (" + account_id + ")")
        log.fatal(e)
        sys.exit()


def get_account_id_field(account_type):
    return str(account_type) + '_ACCOUNT_ID'


def validate_targets(account_type):
    total_weight = 0
    for ticker, weight in get_targets(account_type):
        validate_weight(weight)
        validate_ticker(ticker)
        total_weight += float(weight)
        log.info("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW total_weight: "+str(total_weight))
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
    log.info("Validating if '{0}' is a valid ticker".format(ticker.upper()))
    symbol = questrade.get_symbol(ticker)
    if len(symbol['symbols']) != 1:
        log.fatal(ticker.upper() + " is not a valid ticker")
        sys.exit()
    log.info(ticker.upper() + " is a valid ticker")


def validate_total_weight(total_weight, account_type):
    if total_weight != 1:
        log.error("Total weight your " + account_type + " portfolio: " + str(total_weight))
        log.fatal("Total weight doesn't equal 100%. Please review your tickers/weight and get me back.")
        sys.exit()


def get_account_types():
    return config.sections()


def get_account_id(account_type):
    return os.environ[get_account_id_field(account_type)]


def get_targets(account_type):
    return config[account_type].items()


def load_config(config_path):
    config.read(config_path)
    validate_config()
