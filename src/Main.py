import log4p
import configparser

from api.QuestradeDao import QuestradeDao
from model.Portfolio import Portfolio
from src import ConfigManager

from src.model.AccountType import AccountType


log = log4p.GetLogger(__name__, config="../log4p.json").logger

questrade = QuestradeDao()


def build_portfolio(account_id):
    balances = questrade.get_balances(account_id)
    log.info(str(balances))
    positions = questrade.get_positions(account_id)
    log.info(str(positions))
    return Portfolio(account_id, balances, positions)


def run():
    ConfigManager.load_config('../config.ini')
    account_id = ConfigManager.get_account_id(AccountType.TFSA)
    log.info("WWWWWWWWWWWWWWWW "+account_id)
    portfolio = build_portfolio(str(ConfigManager.get_account_id(AccountType.TFSA)))
    log.info(str(portfolio))


run()
