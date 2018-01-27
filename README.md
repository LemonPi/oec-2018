## Install
`pip install flask`
`pip install pandas`

Alternatively use `python -m pip` instead of just `pip`.
Note this package requires python 3

## Running
`python server.py`

## Accessing Dashboard
1. Enable CORS from browser (in Chrome get the Allow-Control-Allow-Origin extension) (or for the API developer please allow CORS :D)
2. visit `http://uoft-a-oec-2018.herokuapp.com/dashboard`


## Components
### Heroku deployed python server that does
1. automated trading
2. historical price front end for visualization

### Trading algorithm
- mean reversion?
- computing first and second derivatives?
- machine learning?

#### API
for each timestep, trading algorithm
===
input:
account {
    number cash
    [holding {
        string ticker
        number num_shares
        number book_price
        number market_price
    }]
}
[stocks {
    string ticker
    number [historical price] or current price if past prices known
}]
===
outputs:
[action {
    string type "buy" | "sell",
    string ticker
    number num_shares
}]
