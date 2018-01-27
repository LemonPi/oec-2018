from flask import Flask, render_template
from algo import DerivativeTradingAlgo
import api
import time

app = Flask(__name__)

app.debug = True


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/trade")
def trade():
    starttime = time.time()
    while True:
        print("tic")
        trade()
        print("toc")
        time.sleep(60.0 - ((time.time() - starttime) % 60.0))
    return "Success"

WINDOW = 2
algo = DerivativeTradingAlgo(WINDOW, 0.05, 0.05)
CARE_ABOUT_LAST = WINDOW * 5


def trade():
    """Called every external network update (60s) to run trading algorithm"""
    account = api.get_account()
    tickers = api.list_tickers()
    stocks = []

    # we prefiltered the list for high fluctuation tickers
    # since the API is very slow, querying the price of all tickers each time is not feasible
    # instead we'll only care about high fluctuation stocks
    MED_FLUCTUATION_TICKERS = ['SLC', 'ILV', 'WIQ', 'KWM', 'DMP', 'FVN', 'KIY', 'EVI', 'QSY', 'FIT', 'YHG', 'DRZ',
                               'VDH', 'UJY', 'PSO', 'SFY', 'IJL', 'PFY', 'CDL', 'YWA', 'BDZ', 'NBH', 'UWG', 'OGN',
                               'TCS', 'VFP', 'HYB', 'UIZ', 'WHD', 'UQN', 'WKZ', 'OUR', 'WGO', 'DBC', 'KBM', 'VPQ',
                               'MPB', 'LAZ', 'LEY', 'FZO', 'XKD', 'MOP', 'SDU', 'EFQ', 'QXU', 'UFB', 'KBP', 'GSH',
                               'OPZ', 'LFW', 'VAI', 'JTX', 'IYG', 'HQB', 'FNJ', 'CMQ', 'BVY', 'OGW', 'JOC', 'DYJ',
                               'PVE', 'MOE', 'CRA', 'NVF', 'WZF', 'JYW', 'SJO', 'VAW', 'DCU', 'UPQ', 'KYI', 'RSV',
                               'WOX', 'JXV', 'DCR', 'VJU', 'UTA', 'LWV', 'LCH', 'BHP', 'CYE', 'LYS', 'QZL', 'HQK',
                               'IZA', 'HDA', 'LOT', 'POQ', 'VMA', 'QZT', 'TJX', 'FIG', 'PAH', 'SWN', 'KIV', 'PHA',
                               'SPJ', 'CQJ', 'NTK', 'KVQ', 'CRH', 'ARW', 'AIU', 'UIN', 'HYS', 'DRM', 'OLE', 'KRA',
                               'KEG', 'BVJ', 'QEL', 'OLS', 'LDO', 'KIR', 'UWB', 'URY', 'KXU', 'FYS', 'GXF', 'KQS',
                               'GBO', 'YTD', 'JAR', 'SPQ', 'RBH', 'MTG', 'KJX', 'VGL', 'AES', 'OVM']
    HIGH_FLUCTUATION_TICKERS = ['KWM', 'DMP', 'FVN', 'QSY', 'FIT', 'YHG', 'VDH', 'UJY', 'PSO', 'IJL', 'PFY', 'CDL',
                                'YWA', 'BDZ', 'UWG', 'VFP', 'HYB', 'UIZ', 'WHD', 'WKZ', 'OUR', 'WGO', 'KBM', 'VPQ',
                                'LAZ', 'LEY', 'XKD', 'QXU', 'OPZ', 'JTX', 'IYG', 'RSV', 'LWV', 'POQ', 'KVQ', 'FYS',
                                'GXF']

    for ticker in HIGH_FLUCTUATION_TICKERS:
        prices = api.get_prices(ticker)
        last_prices = prices[-CARE_ABOUT_LAST:]
        print("got {}, last prices: {}".format(ticker, last_prices))
        stocks.append({'ticker': ticker, 'historical_price': last_prices})

    print("got prices")

    actions = algo.step(account, stocks)
    for action in actions:
        print(action)
        take_action(action)


def take_action(action):
    """Take a buy/sell action commanded by trading algo via network API"""
    if action.type == 'buy':
        print("buy {} stocks of {}".format(action.num_shares, action.ticker))
        api.buy_stock(action.ticker, action.num_shares)
    elif action.type == 'sell':
        print("sell {} stocks of {}".format(action.num_shares, action.ticker))
        api.sell_stock(action.ticker, action.num_shares)


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
