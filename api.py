"""
Python translated API of external trading service.
Raises exceptions on any errors
"""
from data_structures import Account, Holding
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


def request(url_pieces, extra_params={}):
    """Make a get request
    [string],{} -> Request"""

    def join_urls(pieces):
        return '/'.join(s.strip('/') for s in pieces)

    # merge the two lists; we'll always need host
    urls = [HOST]
    urls.extend(url_pieces)

    # merge the two dictionaries; we'll always need to give key
    params = {'key': KEY}
    params.update(extra_params)

    r = requests.get(join_urls(urls), params=params).json()
    reject_bad_requests(r)

    return r


def list_tickers():
    """List all stock tickers
    -> [string]"""
    r = request([STOCK, 'list'])
    return r['stock_tickers']


def get_prices(ticker):
    """Get historical prices (including current) of given stock in cents
    Last element in list is current price
    string -> [number]"""
    r = request([STOCK], {'ticker': ticker})
    return r['historical_price']


def buy_stock(ticker, num_shares):
    """Buy num_shares of given stock"""
    request(['buy'], {'ticker': ticker, 'shares': num_shares})


def sell_stock(ticker, num_shares):
    """Sell num_shares of given stock"""
    request(['sell'], {'ticker': ticker, 'shares': num_shares})


def get_account():
    """Get account information
    -> Account"""
    acc = Account()
    r = request(['account'])
    acc.cash = r['cash']

    for holding in r['holdings']:
        h = Holding(holding['ticker'], holding['shares'], holding['book_cost'], holding['market_value'])
        acc.holdings.append(h)

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
        
if __name__ == "__main__":
    # Change this arg to True to update batchprices.pickle
    get_batch_prices(True)

