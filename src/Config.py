import log4p
import configparser
import os

from src.api.Questrade import Questrade
from src.model.enum.AccountType import AccountType

log = log4p.GetLogger(__name__, config="../log4p.json").logger
config = configparser.ConfigParser()
questrade = Questrade()
accounts = questrade.get_accounts()


def load(config_path):
    config.read(config_path)
    for account_type in get_account_types():
        validate_account_type(account_type)
        validate_account(get_account_id(account_type))
        validate_targets(account_type)


def validate_account_type(account):
    if account.upper() not in AccountType.__members__:
        raise ValueError("Account type " + account + " is not a valid account type")


def validate_account(account_id):
    if int(account_id) > 99999999 or int(account_id) < 10000000:
        raise ValueError("Questrade account id must be a 8 digits number - current value" + account_id)
    if not is_valid_account(account_id):
        raise ValueError("Questrade account " + account_id + " is not active or was not found")


def is_valid_account(account_id):
    for account in accounts:
        if account["number"] == str(account_id):
            if account["status"] == "Active":
                return True


def get_account_id_field(account_type):
    return str(account_type) + '_ACCOUNT_ID'


def validate_targets(account_type):
    total_weight = 0
    for ticker, weight in get_targets(account_type):
        validate_weight(weight)
        validate_ticker(ticker)
        total_weight += float(weight)
    validate_total_weight(total_weight, account_type)


def validate_weight(weight):
    if float(weight) < 0:
        raise ValueError("The weight of a symbol can't be below zero - current value" + weight)


def validate_ticker(ticker):
    if len(questrade.get_symbol(ticker)['symbols']) != 1:
        raise ValueError(ticker.upper() + " is not a valid ticker, not found on Questrade")


def validate_total_weight(total_weight, account_type):
    if round(total_weight, 2) != 1.00:
        raise ValueError("Total weight for account " + account_type
                         + " doesn't equal 1.00 - current value" + str(total_weight))


def get_account_types():
    return config.sections()


def get_account_id(account_type):
    return os.environ[get_account_id_field(account_type)]


def get_targets(account_type):
    return config[account_type].items()


def get_target(account_type, ticker):
    return config[account_type][ticker]
