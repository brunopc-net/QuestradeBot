from app.model.Position import Position


class Portfolio:

    def __init__(self, account_id, account_balances, account_positions):
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
            weight = pos.currentMarketValue / self.total_value
            pos.set_weight(weight)

    def __repr__(self):
        return {'balance': str(self.balance), 'positions': self.positions}

    def __str__(self):
        portfolio_str = "Portfolio(balance=" + str(self.balance) + ",positions=\n"
        for pos in self.positions:
            portfolio_str += "\t" + pos.__str__() + ",\n"
        portfolio_str += ", total_value=" + format(self.total_value, '.2f') + ")"
        return portfolio_str
