import log4p

from api.QuestradeDao import QuestradeDao
from src import Config
from src.builder import PortfolioBuilder
from src.builder.OrderBuilder import OrderBuilder

log = log4p.GetLogger(__name__, config="../log4p.json").logger

Questrade = QuestradeDao()

CONFIG_FILE = '../config.ini'


def run():
    Config.load(CONFIG_FILE)
    for account_type in Config.get_account_types():
        portfolio = PortfolioBuilder.build(account_type)
        orders = OrderBuilder(portfolio).build_orders()


run()
