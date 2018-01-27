"""
Python translated API of external trading service.
Raises exceptions on any errors
"""
from data_structures import Account

import requests
import matplotlib.pyplot as plt

KEY = '0MJ5v-KSNMbINd3EB5H_Ew'
<<<<<<< HEAD
HOST = 'http://oec-2018.herokuapp.com/api/stock'
=======
HOST = 'http://oec-2018.herokuapp.com/api/'
>>>>>>> 31f905b85d26c7f7245cb5b8235f474e19a46985


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

def get_batch_prices():
    """Get all historical prices for all current stocks"""

    d= {}

    r = requests.get(HOST + "/list", params={"key":KEY}).json()
    for ticker in r["stock_tickers"]:
        r=requests.get(HOST, params={
            "ticker":ticker,
            "key":KEY
        }).json()
        d[ticker] = r["historical_price"]
    
    i = 1
    for p in d:
        plt.plot(d[p])
        plt.ylabel(p)
        plt.subplot(6,5,i)
        i += 1

    plt.show()
    
if __name__ == "__main__":
    get_batch_prices()

