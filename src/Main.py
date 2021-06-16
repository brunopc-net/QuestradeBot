import log4p

from api.QuestradeDao import QuestradeDao
from src import Config
from src.builder import PortfolioBuilder
from src.builder.OrderBuilder import OrderBuilder

log = log4p.GetLogger(__name__, config="../log4p.json").logger

Questrade = QuestradeDao()

CONFIG_FILE = '../config.ini'
ORDER_EXEC_LIMIT_TIME = 10


def run():
    Config.load(CONFIG_FILE)
    for account_type in Config.get_account_types():
        portfolio = PortfolioBuilder.build(account_type)
        orders = OrderBuilder(portfolio).build_orders()

'''
def is_last(portfolio, position):
    last_symbol = portfolio.positions[len(portfolio.positions) - 1]['symbolId']
    return position['symbolId'] == last_symbol



def post_order(order):
    order_resp = Questrade.post_order(order)
    if order_resp["state"] != "Accepted":
        log.fatal("The order status wasn't accepted, actual status: " + order_resp["state"])
        sys.exit()
    while order_resp["state"] != "Executed":
        log.info("Waiting for the order to execute, current status: " + order_resp["state"])
        order_resp = Questrade.get_order(order.accountNumber, order_resp["id"])
            log.fatal("The order wasn't able to execute")
        time.sleep(1)
    return False
'''


def money(amount):
    return "$" + format(amount, '.2f')


run()
