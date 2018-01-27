
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
        balance = 100000
        holdings = {}

        for tick, price_list in d.items():
            if len(price_list) > mx:
                mx = len(price_list)

        for i in range(mx, 0, -1):
            prices[i] = {}

            for tick, price_list in d.items():
                if len(price_list) > mx - i:
                    prices[i][tick] = p_list[-(mx-i)-1]

        print(prices)
        wym = []
        for i in range(1, mx):
            if "WYM" in prices[i]:
                wym.append(prices[i]["WYM"])

        for i in range(1, mx):
            pass
            #put day-by-day sim here
            # use holdings and balance vars
