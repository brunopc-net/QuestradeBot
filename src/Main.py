import sys
import log4p

from src import Config
from src.builder import PortfolioBuilder
from src.builder.OrderBuilder import OrderBuilder

log = log4p.GetLogger(__name__, config="../log4p.json").logger

CONFIG_FILE = '../config.ini'
ORDER_EXEC_LIMIT_TIME = 10

try:
    Config.load(CONFIG_FILE)
except ValueError as ve:
    log.fatal(ve)
    sys.exit()

for account_type in Config.get_account_types():
    portfolio = PortfolioBuilder.build(account_type)
    orders = OrderBuilder(portfolio).build_orders()
