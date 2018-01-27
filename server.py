from flask import Flask, render_template
import api

app = Flask(__name__)

app.debug = True


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


def take_action(action):
    """Take a buy/sell action commanded by trading algo via network API"""
    if action.type == 'buy':
        api.buy_stock(action.ticker, action.num_shares)
    elif action.type == 'sell':
        api.sell_stock(action.ticker, action.num_shares)


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
