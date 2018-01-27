"""
Python translated API of external trading service.
Raises exceptions on any errors
"""

KEY = '0MJ5v-KSNMbINd3EB5H_Ew'
HOST = 'http://oec-2018.herokuapp.com/api/stock/'


def list_tickets():
    """List all stock tickets
    -> [string]"""
    return []


def get_prices(stock_ticket):
    """Get historical prices (including current) of given stock in cents
    Last element in list is current price
    string -> [number]"""
    return 0


def buy_stock(stock_ticket, num_shares):
    """Buy num_shares of given stock"""


def sell_stock(stock_ticket, num_shares):
    """Sell num_shares of given stock"""
