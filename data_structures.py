from collections import namedtuple

Holding = namedtuple("Holding", "ticker shares book_cost market_value")
Action = namedtuple("Action", "type ticker num_shares")

class Account:
    def __init__(self):
        self.cash = 10000000
        self.holdings = []
