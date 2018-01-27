"""
Python translated API of external trading service.
Raises exceptions on any errors
"""
from data_structures import Account
import os
import requests
import matplotlib.pyplot as plt
import pickle

KEY = '0MJ5v-KSNMbINd3EB5H_Ew'
HOST = 'http://oec-2018.herokuapp.com/api'


def list_tickers():
    """List all stock tickers
    -> [string]"""
    return []


def get_prices(ticker):
    """Get historical prices (including current) of given stock in cents
    Last element in list is current price
    string -> [number]"""
    return 0


def buy_stock(ticker, num_shares):
    """Buy num_shares of given stock"""


def sell_stock(ticker, num_shares):
    """Sell num_shares of given stock"""

def get_account():
    """Get account information
    -> Account"""
    acc = Account()
    return acc

def get_batch_prices(update):
    """Get all historical prices for all current stocks"""

    d= {}

    if os.path.isfile('batchprices.pickle') and not update:
        with open('batchprices.pickle', 'rb') as handle:
            d = pickle.load(handle)

    else:
        r = requests.get(HOST + "/stock/list", params={"key":KEY}).json()
        for ticker in r["stock_tickers"]:
            r=requests.get(HOST + "/stock", params={
                "ticker":ticker,
                "key":KEY
            }).json()
            d[ticker] = r["historical_price"]

        with open('batchprices.pickle', 'wb') as handle:
            pickle.dump(d, handle, protocol=pickle.HIGHEST_PROTOCOL)

    i = 1
    for p in d:
        plt.subplot(6,5,i)
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
        
if __name__ == "__main__":
    get_batch_prices(False)

