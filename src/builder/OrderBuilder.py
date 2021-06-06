from math import floor

import log4p

from src import Config
from src.model.Order import Order

log = log4p.GetLogger(__name__, config="../log4p.json").logger

# We set a limit price a couple of cents more then the current price for 3 reasons:
# 1- We don't want to overpay if a sudden, temporary price spike is occurring
# 2- We want to avoid sudden small spikes to block the trade
# 3- Position current price from the API may be a bit delayed
LIMIT_UPPER_PRICE = 0.05


class OrderBuilder(object):

    def __init__(self, portfolio):
        self.portfolio = portfolio
        self.cash = portfolio.balance

    def build_orders(self):
        log.info(
            "Building orders for " + self.portfolio.account_type + " portfolio, "
            + "Balance: " + money(self.portfolio.balance)
        )
        orders = []
        for position in self.portfolio.positions:
            order = self.__build_order(position)
            if order is not None:
                orders.append(order)
                self.cash -= order.get_amount()
                log.info("Cash remaining: " + money(self.cash))
        log.info("Building orders for " + self.portfolio.account_type + " portfolio: DONE")
        return orders

    def __build_order(self, position):
        order_qty = self.__get_quantity(position)
        if order_qty == 0:
            return None
        order = Order(
            self.portfolio.account_id,
            position['symbolId'],
            order_qty,
            self.__get_limit_price(position)
        )
        log.info("New order created - amount " + money(order.get_amount()) + " " + str(order))
        return order

    def __get_quantity(self, position):
        order_amount = self.__get_amount(self.portfolio, position)
        if order_amount < position['currentPrice']:
            log.info("Not enough cash to buy " + position['symbol'] +
                     " - current value: " + money(position['currentPrice']))
            return 0
        return floor(order_amount / self.__get_limit_price(position))

    def __get_amount(self, portfolio, position):
        position_target_weight = Config.get_target(portfolio.account_type, position['symbol'])
        position_target_amount = float(position_target_weight) * portfolio.total_value
        log.info("Position " + position['symbol'] + ": target_weight=" + str(position_target_weight) +
                 ", target_amount=" + money(position_target_amount))
        position_target_buy = position_target_amount - position['currentMarketValue']
        return min(position_target_buy, self.cash)

    def __get_limit_price(self, position):
        return float(position['currentPrice'] + LIMIT_UPPER_PRICE)


def money(amount):
    return "$" + format(amount, '.2f')
