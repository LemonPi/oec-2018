"""
Python translated API of external trading service.
Raises exceptions on any errors
"""
from data_structures import Account

KEY = '0MJ5v-KSNMbINd3EB5H_Ew'
HOST = 'http://oec-2018.herokuapp.com/api/'


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