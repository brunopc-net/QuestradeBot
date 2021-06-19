import unittest
import log4p

from src import Config
from src.api.Questrade import Questrade
from src.builder.OrderBuilder import OrderBuilder
from src.model.object.Portfolio import Portfolio
from src.model.object.Position import Position

log = log4p.GetLogger(__name__, config="../log4p.json").logger

Questrade = Questrade()


class TestQuestradeBot(unittest.TestCase):

    def test_order_builder(self):
        # GIVEN an unbalanced portfolio of three positions
        Config.load("config_test_order_builder.ini")
        portfolio = Portfolio(
            "TFSA",
            8465498,
            [
                Position({
                    "symbol": "VCN.TO",
                    "symbolId": 4278411,
                    "openQuantity": 75,
                    "currentMarketValue": 2480.25,
                    "currentPrice": 33.07,
                    "averageEntryPrice": 20.15,
                    "openPnl": 311,
                    "closedPnl": 0,
                    "totalCost": 2015
                }),
                Position({
                    "symbol": "XAW.TO",
                    "symbolId": 8953193,
                    "openQuantity": 100,
                    "currentMarketValue": 2326,
                    "currentPrice": 23.26,
                    "averageEntryPrice": 20.15,
                    "openPnl": 311,
                    "closedPnl": 0,
                    "totalCost": 2015
                }),
                Position({
                    "symbol": "ZAG.TO",
                    "symbolId": 9029,
                    "openQuantity": 188,
                    "currentMarketValue": 2972.28,
                    "currentPrice": 15.81,
                    "averageEntryPrice": 20.15,
                    "openPnl": 311,
                    "closedPnl": 0,
                    "totalCost": 2015
                }),
            ],
            2952.87
        )

        # WHEN building orders
        orders = OrderBuilder(portfolio).build_orders()

        # THEN order quantities are correct
        order_vcn = orders[0]
        order_xaw = orders[1]
        order_zag = orders[2]

        self.assertEqual(22, order_vcn.quantity, "VCN.TO order quantity is expected")
        self.assertEqual(61, order_xaw.quantity, "XAW.TO order quantity is expected")
        self.assertEqual(50, order_zag.quantity, "ZAG.TO order quantity is expected")

        # AND balance is correct
        self.assertEqual(round(portfolio.balance, 2), 9.32, "Balance remaining is expected")

    def test_invalid_config(self):
        # GIVEN valid config
        config_file = '../config.ini'
        # WHEN loading
        Config.load(config_file)
        # THEN no Error

    def test_valid_config(self):
        # GIVEN valid config
        config_file = '../config.ini'
        # WHEN loading
        Config.load(config_file)
        # THEN no Error


if __name__ == '__main__':
    unittest.main()
