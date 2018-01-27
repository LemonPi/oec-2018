from data_structures import Account
from calculus import filter_out_smooth_stocks

class Simulator:
"""
The simulator allows for the testing of trading algorithms
by assessing the algorithm's performance across historical data.
"""
    def __init__(self, trading_algo):
        self.trading_algo = trading_algo

    def simulate():
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
                    prices[i][tick] = p_list[-(mx-i)-1]

        filtered_prices = filter_out_smooth_stocks(0.98)

        for i in range(1, mx):
            stocks = []
            for ticker in filtered_prices:
                historical_price = []
                for j in range(1,i):
                    historical_price.append(prices[j][ticker])
                
                stocks.append({'ticker':ticker, 'histortical_price':historical_price})
            self.trading_algo.step(account, stocks)

if __name__ == "__main__":
