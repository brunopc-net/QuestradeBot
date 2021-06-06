class Portfolio:

    def __init__(self, account_type, account_id, positions, balance):
        self.account_type = account_type
        self.account_id = account_id
        self.positions = positions
        self.balance = balance
        self.total_value = self.__get_total_value()

    def get_weight(self, symbol):
        return self.get_position(symbol).currentMarketValue / self.total_value

    def get_position(self, symbol):
        for position in self.positions:
            if position.symbol == symbol:
                return position
        return None

    def __get_total_value(self):
        total_value = self.balance
        for position in self.positions:
            total_value += position['currentMarketValue']
        return total_value

    def __repr__(self):
        return {
            'account_type': self.account_type,
            'account_id': self.account_id,
            'balance': str(self.balance),
            'positions': self.positions
        }

    def __str__(self):
        portfolio_str = "Portfolio(account=" + self.account_type \
                        + ", balance=" + Portfolio.money(self.balance) \
                        + ", Positions:\n "
        for pos in self.positions:
            portfolio_str += "\t" + pos.__str__() + ",\n"
        portfolio_str += ", total_value=" + Portfolio.money(self.total_value) + ")"
        return portfolio_str

    @staticmethod
    def money(amount):
        return "$" + format(amount, '.2f')
