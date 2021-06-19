import json


class Symbol(object):

    def __init__(self, symbol_json):
        self.symbol = symbol_json.symbol,
        self.symbolId = symbol_json.symbolId,
        self.description = symbol_json.description,
        self.securityType = symbol_json.securityType,
        self.listingExchange = symbol_json.listingExchange,
        self.isTradable = symbol_json.isTradable,
        self.isQuotable = symbol_json.isQuotable,
        self.currency = symbol_json.currency

    def __repr__(self):
        return {
            "symbol": self.symbol,
            "symbolId": self.symbolId,
            "description": self.description,
            "securityType": self.securityType,
            "listingExchange": self.listingExchange,
            "isTradable": self.isTradable,
            "isQuotable": self.isQuotable,
            "currency": self.currency
        }

    def __str__(self):
        return json.dumps(self.__dict__)
