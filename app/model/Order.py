import json


class Order(object):

    def __init__(self, account_id, symbol_id, quantity, limit_price):
        self.__dict__ = {
            "accountNumber": account_id,
            "symbolId": symbol_id,
            "quantity": quantity,
            "limitPrice": format(limit_price, '.2f'),
            "isAllOrNone": True,
            "isAnonymous": False,
            "orderType": "Limit",
            "timeInForce": "Day",
            "action": "Buy",
            "primaryRoute": "AUTO",
            "secondaryRoute": "AUTO",
            "amount": format(quantity * limit_price, '.2f')
        }

    def __repr__(self):
        return self.__dict__

    def __str__(self):
        return json.dumps(self.__dict__)
