import log4p

from src import Config

from src.api.Questrade import Questrade
from src.model.object.Portfolio import Portfolio
from src.model.object.Position import Position

log = log4p.GetLogger(__name__, config="../log4p.json").logger
Questrade = Questrade()


def build(account_type):
    account_id = str(Config.get_account_id(account_type))
    portfolio = Portfolio(
        account_type,
        account_id,
        get_positions(account_id),
        get_balance(account_id)
    )
    # Sorting the position by price desc
    # Buying the most expensive trades first for the cash is efficiently used
    portfolio.positions.sort(key=lambda pos: pos.currentPrice, reverse=True)
    log.info("Portfolio loaded: " + account_type + " " + str(portfolio))
    return portfolio


def get_positions(account_id):
    positions = []
    for position in Questrade.get_positions(account_id):
        positions.append(Position(position))
    return positions


def get_balance(account_id):
    return Questrade.get_balance(account_id, 'CAD')
