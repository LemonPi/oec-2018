import pandas as pd
import pickle
import matplotlib.pyplot as plt
import math
import api


def window_stats(historical_price, window, plot=False):
    if len(historical_price) == 0:
        return 0, 0

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


def filter_out_smooth_stocks(smooth_threshold, plot=False):
    d = {}
    with open('batchprices.pickle', 'rb') as handle:
        d = pickle.load(handle)

    ok = []

    for tick in d:
        s = pd.Series(d[tick])
        if s.autocorr(lag=1) > 0.01:
            # print(tick, math.log(s.autocorr(lag=1)) * 100)
            if math.log(s.autocorr(lag=1)) < -smooth_threshold:
                ok.append(tick)

    if plot:
        i = 1
        for p in d:
            plt.subplot(20, 10, i)
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

    return ok


if __name__ == "__main__":
    # buy_or_sell(0.98)
    print(window_stats(api.get_prices('OPZ'), 3))
