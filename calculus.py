import pandas as pd
import pickle 
import matplotlib.pyplot as plt
import math

class dfdt:
	def first_d(prices, index, dx):
		# computes first derivative = (f(x) - f(x-dx))/dx
		# assumes index > 0
		return (prices[index] - prices[index-1])/dx

	def second_d(prices, index, dx):
		# compute second derivative = (f(x) - 2f(x-dx) + f(x-2dx))/dx^2
		# assumes index > 1
		return (prices[index] - 2*prices[index-1] + prices[index-2])/(dx**2)

def buy_or_sell(smooth_threshold):

	d = {}
	with open('batchprices.pickle', 'rb') as handle:
		d = pickle.load(handle)

	ok = []

	for tick in d:
		s = pd.Series(d[tick])
		print(tick, math.log(s.autocorr(lag=1))*100)
		if math.log(s.autocorr(lag=1)) < -0.01:
			ok.append(tick)
	i = 1
	for p in d:
		plt.subplot(6,5,i)
		plt.plot(d[p])
		plt.ylabel(p)
		if i == 2:
			print(p)
		plt.subplot(6, 5, i)
		i += 1

	print(i)
	print(len(d))
	plt.subplots_adjust(left=0.07, bottom=0.04, right=0.98, top=0.96,
				wspace=0.4, hspace=0.4)
	mng = plt.get_current_fig_manager()
	mng.resize(*mng.window.maxsize())
	plt.show()
		
if __name__ == "__main__":
	buy_or_sell(0.98)