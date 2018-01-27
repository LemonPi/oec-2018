from data_structures import Account, Holding
from calculus import filter_out_smooth_stocks
from algo import DerivativeTradingAlgo
from api import COST_PER_ACTION
import pickle


class Simulator:
    """
    The simulator allows for the testing of trading algorithms
    by assessing the algorithm's performance across historical data.
    """

    def __init__(self, trading_algo):
        self.trading_algo = trading_algo

    def simulate(self):
        d = {}
        with open('batchprices.pickle', 'rb') as handle:
            d = pickle.load(handle)

        prices = {}
        mx = 0
        account = Account()

        for tick, price_list in d.items():
            if len(price_list) > mx:
                mx = len(price_list)

        for i in range(mx, 0, -1):
            prices[i] = {}

            for tick, price_list in d.items():
                if len(price_list) > mx - i:
                    prices[i][tick] = price_list[-(mx - i) - 1]

        filtered_prices = filter_out_smooth_stocks(0.01)

        for i in range(1, mx+1):
            print("simulating hour {}".format(i))
            stocks = []
            for ticker in filtered_prices:
                historical_price = []
                for j in range(1, i):
                    if ticker in prices[j]:
                        historical_price.append(prices[j][ticker])

                stocks.append({'ticker': ticker, 'historical_price': historical_price})
            # print(stocks)
            actions = self.trading_algo.step(account, stocks)
            for action in actions:
                Simulator.take_action(action, account, prices[i])

        Simulator.check_holdings(account, prices[mx])
        return account

    @staticmethod
    def check_holdings(account, prices):
        value = account.cash
        print("cash: {}".format(account.cash))
        for holding in account.holdings:
            print("holding {} shares of {} at {} each".format(holding.shares, holding.ticker, prices[holding.ticker]))
            value += prices[holding.ticker] * holding.shares
        print("total value: {}".format(value))

    @staticmethod
    def take_action(action, account, prices):
        if action.type == 'buy':
            print("buying {} shares of {}".format(action.num_shares, action.ticker))
            # print(prices)
            cost = action.num_shares * prices[action.ticker]
            if cost + COST_PER_ACTION > account.cash:
                print("ERROR trying to buy more stocks than we can buy")
            else:
                h = Holding(action.ticker, action.num_shares, prices[action.ticker], prices[action.ticker])
                account.cash -= cost
                account.holdings.append(h)

        elif action.type == 'sell':
            print("selling {} shares of {}".format(action.num_shares, action.ticker))

            cash_plus = 0
            for holding in account.holdings:
                if holding.ticker == action.ticker:
                    cash_plus += action.num_shares * prices[action.ticker]

            # trying to sell something but we don't have any of it
            if cash_plus == 0:
                print("ERROR trying to sell {} but we don't have any of it".format(action.ticker))
            else:
                cash_plus -= COST_PER_ACTION
                account.cash += cash_plus
                account.holdings = [holding for holding in account.holdings if holding.ticker != action.ticker]


if __name__ == "__main__":
    sim = Simulator(DerivativeTradingAlgo(2, 0.05, 0.05))
    sim.simulate()
