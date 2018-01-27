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
STOCK = 'stock'
ACCOUNT = 'account'

class RequestError(Exception):
    def __init__(self, message):
        super(RequestError, self).__init__(message)


def reject_bad_requests(r):
    """Raise an exception on any response with errors"""
    if not r['success']:
        raise RequestError('/n'.join(r['errors']))


def join_urls(pieces):
    return '/'.join(s.strip('/') for s in pieces)


def list_tickers():
    """List all stock tickers
    -> [string]"""
    r = requests.get(join_urls([HOST, STOCK, 'list']), params={'key': KEY}).json()
    reject_bad_requests(r)

    return r['stock_tickers']


def get_prices(ticker):
    """Get historical prices (including current) of given stock in cents
    Last element in list is current price
    string -> [number]"""
    r = requests.get(join_urls([HOST, STOCK]), params={'key': KEY, 'ticker': ticker}).json()
    reject_bad_requests(r)

    return r['historical_price']


def buy_stock(ticker, num_shares):
    """Buy num_shares of given stock"""
    r = requests.get(join_urls([HOST, 'buy']), params={'key': KEY, 'ticker': ticker, 'shares': num_shares}).json()
    reject_bad_requests(r)


def sell_stock(ticker, num_shares):
    """Sell num_shares of given stock"""
    r = requests.get(join_urls([HOST, 'sell']), params={'key': KEY, 'ticker': ticker, 'shares': num_shares}).json()
    reject_bad_requests(r)


def get_account():
    """Get account information
    -> Account"""
    acc = Account()
    return acc

def get_batch_prices(update):
    """Get all historical prices for all current stocks"""

    d = {}

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
    get_batch_prices(False)

