import json


class Order(object):

    def __init__(self, account_id, symbol_id, quantity, limit_price):
        self.accountNumber = account_id
        self.symbolId = symbol_id
        self.quantity = quantity
        self.limitPrice = limit_price
        self.isAllOrNone = True
        self.isAnonymous = False
        self.orderType = "Limit"
        self.timeInForce = "Day"
        self.action = "Buy"
        self.primaryRoute = "AUTO"
        self.secondaryRoute = "AUTO"

    def get_amount(self):
        return self.quantity * self.limitPrice

    def __repr__(self):
        return {
            "accountNumber": self.accountNumber,
            "symbolId": self.symbol_id,
            "quantity": self.quantity,
            "limitPrice": self.limitPrice,
            "isAllOrNone": self.isAllOrNone,
            "isAnonymous": self.isAnonymous,
            "orderType": self.orderType,
            "timeInForce": self.timeInForce,
            "action": self.action,
            "primaryRoute": self.primaryRoute,
            "secondaryRoute": self.secondaryRoute
        }

    def __str__(self):
        return json.dumps(self.__dict__)
