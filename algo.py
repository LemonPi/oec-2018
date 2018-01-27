from calculus import window_stats
import math


class TradingAlgo:
    def __init__(self):
        pass

    def step(self, account, stocks):
        raise NotImplementedError

    def add_action(self, actions, type, ticker, num_stocks):
        actions.append({
            'type': type,
            'ticker': ticker,
            'number_shares': num_stocks
        })

class DerivativeTradingAlgo(TradingAlgo):
    def __init__(self, window, d_threshold, dd_threshold):
        """
        :param window: Size of smoothing window
        :param d_threshold: Threshold for normalized derivative below which the stock becomes interesting
        :param dd_threshold: Threshold for normalized second derivative above which we buy stock and below the negative
        of which we sell stock
        """
        self.window = window
        self.d_threshold = d_threshold
        self.dd_threshold = dd_threshold

    def step(self, account, stocks):
        # interesting stocks are the ones with derivatives near 0
        # sell stocks with negative second derivative (curving down), so at peak price
        # buy stocks with positive second derivative (curvature up)
        options = {}
        buy_stocks = []
        sell_stocks = []

        own_stocks = {holding.ticker: holding for holding in account.holdings}

        for stock in stocks:
            (d, dd) = window_stats(stock['historical_price'], self.window)
            ticker = stock['ticker']

            options[ticker] = {'d': d, 'dd': dd}

            if math.fabs(d) < self.d_threshold:
                if dd > self.dd_threshold:
                    buy_stocks.append(stock)
                elif ticker in own_stocks and dd < -self.dd_threshold:
                    sell_stocks.append(stock)

        actions = []
        for stock in sell_stocks:
            ticker = stock['ticker']
            self.add_action(actions, 'sell', ticker, own_stocks[ticker].num_stocks)

        # to guard against risk, allow only half of our money to be spent per time step
        # for now distribute evenly amongst stocks
        cash_per_stock = account.cash / (2 * len(buy_stocks))
        for stock in buy_stocks:
            num_stocks = math.floor(stock['historical_price'][-1] / cash_per_stock)
            self.add_action(actions, 'buy', ticker, num_stocks)

        return actions
