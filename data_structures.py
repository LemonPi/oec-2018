from collections import namedtuple

Stock = namedtuple("Stock", "ticker shares book_cost market_value")


class Account:
    def __init__(self):
        self.cash = 10000000
        self.holdings = []
