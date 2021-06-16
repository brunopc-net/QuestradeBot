import log4p

from src import Config
from src.model.Portfolio import Portfolio, Questrade

log = log4p.GetLogger(__name__, config="../log4p.json").logger


def build(account_type):
    account_id = str(Config.get_account_id(account_type))
    portfolio = Portfolio(
        account_type,
        account_id,
        Questrade.get_positions(account_id),
        Questrade.get_balance(account_id, 'CAD')
    )
    # Sorting the position by price desc
    # Buying the most expensive trades first for the cash is efficiently used
    portfolio.positions.sort(key=lambda pos: pos['currentPrice'], reverse=True)
    log.info("Portfolio loaded: " + account_type + " " + str(portfolio))
    return portfolio
