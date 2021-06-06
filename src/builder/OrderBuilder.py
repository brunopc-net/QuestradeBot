import log4p

from src import Config
from src.model.Order import Order

log = log4p.GetLogger(__name__, config="../log4p.json").logger

# We set a limit price a couple of cents more then the current price for 3 reasons:
# 1- We don't want to overpay if a sudden, temporary price spike is occurring
# 2- We want to avoid sudden small spikes to block the trade
# 3- Position current price from the API may be a bit delayed
LIMIT_UPPER_PRICE = 0.05


def build_orders(portfolio):
    log.info(
        "Building orders for " + portfolio.account_type + " portfolio, Balance: " + money(portfolio.balance))
    orders = []
    for position in portfolio.positions:
        order = __build_order(portfolio, position)
        if order is not None:
            orders.append(order)
            portfolio.balance -= float(order.amount)
            log.info("Portfolio balance reduced to " + format(portfolio.balance, '.2f'))
    log.info("Building orders for " + portfolio.account_type + " portfolio: DONE")
    return orders


def __build_order(portfolio, position):
    order_qty = __get_quantity(portfolio, position)
    if order_qty == 0:
        return None
    order = Order(
        portfolio.account_id,
        position['symbolId'],
        order_qty,
        __get_limit_price(position)
    )
    log.info("New order created: " + str(order))
    return order


def __get_quantity(portfolio, position):
    order_amount = __get_amount(portfolio, position)
    if order_amount < position['currentPrice']:
        log.info("Not enough cash to buy " + position['symbol'] +
                 " - current value: " + money(position['currentPrice']))
        return 0
    return int(round(order_amount / __get_limit_price(position)))


def __get_amount(portfolio, position):
    position_target_weight = Config.get_target(portfolio.account_type, position['symbol'])
    position_target_amount = float(position_target_weight) * portfolio.get_total_value()
    log.info("Position " + position['symbol'] + ": target_weight=" + str(position_target_weight) +
             ", target_amount=" + money(position_target_amount))
    position_target_buy = position_target_amount - position['currentMarketValue']
    return min(position_target_buy, portfolio.balance)


def __get_limit_price(position):
    return position['currentPrice'] + LIMIT_UPPER_PRICE


def money(amount):
    return "$" + format(amount, '.2f')
