
class PortfolioManager:
    
    def __init__(self, broker):
        config.read("broker.get_name()+"_"config.ini")
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
    
