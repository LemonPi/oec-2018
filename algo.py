from calculus import window_stats, get_slope
import math
from data_structures import Action
from api import COST_PER_ACTION


class TradingAlgo:
    def __init__(self):
        pass

    def step(self, account, stocks):
        raise NotImplementedError

    @staticmethod
    def add_action(actions, type, ticker, num_stocks):
        actions.append({
            'type': type,
            'ticker': ticker,
            'number_shares': num_stocks
        })

    @staticmethod
    def buy_stocks(account, stocks):
        """
        Evenly distribute half of remaining money on stocks to buy.
        We don't spend all our money and we distribute amongst other stocks for risk reduction
        :param account:
        :param stocks:
        :return: [Action] list of actions to take
        """
        actions = []
        if stocks:
            cash_per_stock = (account.cash - COST_PER_ACTION) / (2 * len(stocks))
            for stock in stocks:
                num_stocks = math.floor(cash_per_stock / stock['historical_price'][-1])
                if num_stocks > 0:
                    actions.append(Action('buy', stock['ticker'], num_stocks))

        return actions

    @staticmethod
    def sell_stocks(account, stocks):
        """
        Sell all held stocks
        :param account:
        :param stocks:
        :return: [Action] list of actions to take
        """
        own_stocks = {holding.ticker: holding for holding in account.holdings}
        actions = []
        for stock in stocks:
            ticker = stock['ticker']
            actions.append(Action('sell', ticker, own_stocks[ticker].shares))
        return actions


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
                    # print(stock, dd, self.dd_threshold)
                    buy_stocks.append(stock)
                elif ticker in own_stocks:
                    # print(dd)
                    if dd < -self.dd_threshold:
                        sell_stocks.append(stock)

        actions = []

        actions.extend(TradingAlgo.sell_stocks(account, sell_stocks))
        actions.extend(TradingAlgo.buy_stocks(account, buy_stocks))

        return actions


class LinearRegressionAlgo(TradingAlgo):
    def __init__(self, slope_threshold, consider_num_last=100):
        self.slope_threshold = slope_threshold
        self.consider_num_last = consider_num_last

    def step(self, account, stocks):
        """Find the recent slope/linear regress of each stock price"""
        buy_stocks = []
        sell_stocks = []
        own_stocks = {holding.ticker: holding for holding in account.holdings}

        for stock in stocks:
            prices = stock['historical_price'][-self.consider_num_last:]
            # don't do anything on stocks without historical prices
            if not prices:
                continue

            slope = get_slope(range(len(prices)), prices)
            if slope > self.slope_threshold:
                buy_stocks.append(stock)
            elif slope < self.slope_threshold and stock['ticker'] in own_stocks:
                sell_stocks.append(stock)

        actions = []

        actions.extend(TradingAlgo.sell_stocks(account, sell_stocks))
        actions.extend(TradingAlgo.buy_stocks(account, buy_stocks))

        return actions
