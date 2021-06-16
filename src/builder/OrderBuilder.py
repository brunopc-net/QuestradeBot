from math import floor

import log4p

from src import Config
from src.model.Order import Order

log = log4p.GetLogger(__name__, config="../log4p.json").logger

# We set a limit price a couple of cents more then the current price for 3 reasons:
# 1- We don't want to overpay if a sudden, temporary price spike is occurring
# 2- We want to avoid live price increase to block the trade
# 3- Position current price from the API may be a bit delayed
LIMIT_UPPER_PRICE = 0.05


def money(amount):
    return "$" + format(amount, '.2f')


def _get_limit_price(position):
    return float(position['currentPrice'] + LIMIT_UPPER_PRICE)


class OrderBuilder(object):

    def __init__(self, portfolio):
        self.portfolio = portfolio
        self.orders = []

    def build_orders(self):
        log.info(
            "Building orders for " + self.portfolio.account_type + " portfolio, "
            + "Balance: " + money(self.portfolio.balance)
        )
        for position in self.portfolio.positions:
            order = self._build_order(position)
            if order is not None:
                self.orders.append(order)
                self.portfolio.update_balance(order.get_amount())
                log.info("Balance remaining: " + money(self.portfolio.balance))
        log.info("Building orders for " + self.portfolio.account_type + " portfolio: DONE")
        return self.orders

    def _build_order(self, position):
        order_qty = self._get_quantity(position)
        if order_qty == 0:
            return None
        order = Order(
            self.portfolio.account_id,
            position['symbolId'],
            order_qty,
            _get_limit_price(position)
        )
        log.info("New order created - amount " + money(order.get_amount()) + " " + str(order))
        return order

    def _get_quantity(self, position):
        order_room = min(self._get_max_amount(position), self.portfolio.balance)
        if order_room < position['currentPrice']:
            log.info("Not enough room (" + money(order_room) + ") to buy "
                     + position['symbol'] + " (" + money(position['currentPrice']) + ")")
            return 0
        return floor(order_room / _get_limit_price(position))

    def _get_max_amount(self, position):
        position_target_weight = Config.get_target(self.portfolio.account_type, position['symbol'])
        position_target_amount = float(position_target_weight) * self.portfolio.total_value
        log.info("Position " + position['symbol'] + ": target_weight=" + str(position_target_weight) +
                 ", target_amount=" + money(position_target_amount))
        # Setting an overflow limit of half the position price to avoid letting too much leftover money
        overflow_limit = position['currentPrice'] * 0.667
        return position_target_amount - position['currentMarketValue'] + overflow_limit
