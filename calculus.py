
class dfdt:
	def first_d(prices, index, dx):
		# computes first derivative = (f(x) - f(x-dx))/dx
		# assumes index > 0
		return (prices[index] - prices[index-1])/dx

	def second_d(prices, index, dx):
		# compute second derivative = (f(x) - 2f(x-dx) + f(x-2dx))/dx^2
		# assumes index > 1
		return (prices[index] - 2*prices[index-1] + prices[index-2])/(dx**2)