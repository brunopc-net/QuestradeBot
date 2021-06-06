import json


class Position(object):

    def __init__(self, pos_json):
        self.symbol = pos_json.symbol
        self.symbolId = pos_json.symbolId
        self.openQuantity = pos_json.openQuantity
        self.currentMarketValue = pos_json.currentMarketValue
        self.currentPrice = pos_json.currentPrice
        self.averageEntryPrice = pos_json.averageEntryPrice
        self.closedPnl = pos_json.closedPnl
        self.openPnl = pos_json.openPnl
        self.totalCost = pos_json.totalCost
        self.isRealTime = pos_json.isRealTime
        self.isUnderReorg = pos_json.isUnderReorg

    def __repr__(self):
        return {
            "symbol": self.symbol,
            "symbolId": self.symbolId,
            "openQuantity": self.openQuantity,
            "currentMarketValue": self.currentMarketValue,
            "currentPrice": self.currentPrice,
            "averageEntryPrice": self.averageEntryPrice,
            "closedPnl": self.closedPnl,
            "openPnl": self.openPnl,
            "totalCost": self.totalCost,
            "isRealTime": self.isRealTime,
            "isUnderReorg": self.isUnderReorg
        }

    def __str__(self):
        return json.dumps(self.__dict__)
