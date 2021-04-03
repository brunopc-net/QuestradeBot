import log4p
import json
import configparser

from ApiDao import Questrade

log = log4p.GetLogger(__name__).logger
config = configparser.ConfigParser()

TFSA = 'TFSA'
RRSP = 'RRSP'
NONR = 'NONR'

BrokerAPI = Questrade()
    
class Symbol(object):

    def __init__(self, j):
        self.__dict__ = j
    
    def __repr__(self):
        return self.__dict__
    
    def __str__(self):
        return json.dumps(self.__dict__)

class Position(object):

    def __init__(self, j):
        self.__dict__ = j
    
    def set_weight(self, weight):
        self.weight = weight
    
    def __repr__(self):
        return self.__dict__
    
    def __str__(self):
        return json.dumps(self.__dict__)

class Order(object):

    def __init__(self, account_id, symbolId, quantity, limitPrice):
        self.__dict__ = {
            "accountNumber": account_id,
            "symbolId": symbolId,
            "quantity": quantity,
            "limitPrice": format(limitPrice,'.2f'),
            "isAllOrNone": True,
            "isAnonymous": False,
            "orderType": "Limit",
            "timeInForce": "Day",
            "action": "Buy",
            "primaryRoute": "AUTO",
            "secondaryRoute": "AUTO",
            "amount": format(quantity*limitPrice,'.2f')
        }
    
    def __repr__(self):
        return self.__dict__
    
    def __str__(self):
        return json.dumps(self.__dict__)

class Portfolio:

    def __init__(self, account_type, account_id, account_balances, account_positions):
        self.account_type = account_type
        self.account_id = account_id
        self.set_balance(account_balances)
        self.set_positions(account_positions)
        self.set_total_value()
        self.set_positions_weight()
    
    def set_target(self, target):
        self.target = target
    
    def set_balance(self, account_balances):
        for bal in account_balances['perCurrencyBalances']:
            if bal['currency'] == 'CAD':
                self.balance = bal['cash']

    def set_positions(self, account_positions):
        self.positions = []
        for pos in account_positions['positions']:
            position = Position(pos)
            self.positions.append(Position(pos))
    
    def set_total_value(self):
        total = self.balance
        for pos in self.positions:
            total += pos.currentMarketValue
        self.total_value = total
    
    def set_positions_weight(self):
        total = self.balance
        for pos in self.positions:
            weight = pos.currentMarketValue/self.total_value
            pos.set_weight(weight)
        
    def __repr__(self):
        return {'account_type':self.account_type,'balance':str(self.balance),'positions':self.positions}
    
    def __str__(self):
        portfolio_str = "Portfolio(account_type="+self.account_type+",balance="+str(self.balance)+",positions=\n"
        for pos in self.positions:
            portfolio_str += "\t"+pos.__str__()+",\n"
        portfolio_str += ", total_value="+format(self.total_value,'.2f')+")"
        return portfolio_str

class PortfolioManager:
    
    def __init__(self, broker):
        config.read(broker.get_name()+"_config.ini")
        self._broker = broker
        self.orders = []
        self.load_orders()
        
    def load_orders(self):
        for account_type, account_id in config['accounts'].items():
            port = self.get_loaded_portfolio(account_id, account_type.upper())
            self.build_portfolio_orders(port)
        
    def get_loaded_portfolio(self, account_id, account_type):
        balances = self._broker.get_balances(account_id)
        positions = self._broker.get_positions(account_id)
        port = Portfolio(account_type, account_id, balances, positions)
        log.info("New portfolio loaded: "+port.account_type)
        log.info(port.__str__())
        return port
    
    def build_portfolio_orders(self, portfolio):
        log.info("Portfolio "+portfolio.account_type+" orders calculation...")
        for position in portfolio.positions:
            order = self.build_order(portfolio, position)
            if order is not None:
                self.orders.append(order)
                portfolio.balance -= float(order.amount)
                log.info("Portfolio balance reduced to "+format(portfolio.balance,'.2f'))
    
    @classmethod
    def build_order(cls, portfolio, position):
        log.info("Balance remaining for the portfolio: "+format(portfolio.balance,'.2f'))
        target_weight = float(config['targets'][position.symbol])
        target_amount = target_weight*portfolio.total_value
        order_amount = min(target_amount, portfolio.balance)
        log.info("Position "+position.symbol+": target_weight="+str(target_weight)+", target_amount="+format(target_amount,'.2f')+", balance = "+format(portfolio.balance,'.2f'))
        
        if order_amount < position.currentPrice:
            log.info("The position amount to add (value: "+format(order_amount,'.2f')+") do not justify sending an order")
            return
            
        return cls.get_built_order(portfolio.account_id, position.symbolId, order_amount, position.currentPrice)
    
    @staticmethod
    def get_built_order(account_id, symbolId, order_amount, posPrice):
        limitPrice = posPrice + 0.05
        quantity = int(round(order_amount/limitPrice)) 
        order = Order(account_id, symbolId, quantity, limitPrice)
        log.info("New order created for an amount of "+order.amount)
        log.info(order.__str__())
        return order
    
QuestradeAPI = Questrade()
PortfolioManager = PortfolioManager(QuestradeAPI)