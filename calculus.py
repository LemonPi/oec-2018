import pandas as pd
import pickle
import matplotlib.pyplot as plt
import math
import api


class dfdt:
    def first_d(prices, index, dx):
        # computes first derivative = (f(x) - f(x-dx))/dx
        # assumes index > 0
        return (prices[index] - prices[index - 1]) / dx

    def second_d(prices, index, dx):
        # compute second derivative = (f(x) - 2f(x-dx) + f(x-2dx))/dx^2
        # assumes index > 1
        return (prices[index] - 2 * prices[index - 1] + prices[index - 2]) / (dx ** 2)


def window_stats(historical_price, window, plot=False):
    times = range(0, len(historical_price))
    # data = pd.DataFrame(list(zip(times, historical_price)), columns=['Times', 'Price'])
    # prices = data['Price']
    prices = pd.Series(historical_price)
    mavg = prices.rolling(center=False, window=window).mean()

    normalized_mavg = (mavg - mavg.mean()) / mavg.std()

    # first and second derivatives
    derivative = normalized_mavg.diff()
    second_deriv = derivative.diff()

    if plot:
        ax = prices.plot(label='Price')
        mavg.plot(ax=ax, label='Moving avg')
        derivative.plot(ax=ax, label='D')
        plt.scatter(x=times, y=derivative, label='D')
        second_deriv.plot(ax=ax, label='DD')

        ones = pd.Series([0] * len(historical_price))
        ones.plot(ax=ax)

        plt.legend()
        plt.show()

    return derivative.iloc[-1], second_deriv.iloc[-1]

    
def filter_out_smooth_stocks(smooth_threshold):

	d = {}
	with open('batchprices.pickle', 'rb') as handle:
		d = pickle.load(handle)

	ok = []

	for tick in d:
		s = pd.Series(d[tick])
		if s.autocorr(lag=1) > 0.01:
			print(tick, math.log(s.autocorr(lag=1))*100)
		if math.log(s.autocorr(lag=1)) < -0.01:
			ok.append(tick)
	i = 1
	for p in d:
		plt.subplot(20,10,i)
		plt.plot(d[p])
		plt.ylabel(p)
		if i == 2:
			print(p)
		i += 1

	print(i)
	print(len(d))
	plt.subplots_adjust(left=0.07, bottom=0.04, right=0.98, top=0.96,
				wspace=0.4, hspace=0.4)
	mng = plt.get_current_fig_manager()
	mng.resize(*mng.window.maxsize())
	plt.show()

	
def buy_or_sell():

	d = {}
	with open('batchprices.pickle', 'rb') as handle:
		d = pickle.load(handle)

	prices = {}
	mx = 0
	balance = 100000
	holdings = {}

	for tick, p_list in d.items():
		if len(p_list) > mx:
			mx = len(p_list)

	for i in range(mx, 0, -1):
		prices[i] = {}

		for tick, p_list in d.items():
			if len(p_list) > mx - i:
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


if __name__ == "__main__":
    # buy_or_sell(0.98)
    print(window_stats(api.get_prices('OPZ'), 3))
