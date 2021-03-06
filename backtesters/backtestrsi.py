import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from backtestrepository import BacktestRepository
from binancecontroller import BinanceController
from algocollection import *
from twisted.internet import reactor
from binance.websockets import BinanceSocketManager
from binance.client import Client
from enums import *
from datetime import datetime, timezone
import schedule
import btalib
import json

#init environ variables
api_key = os.environ.get('API_KEY')
api_secret = os.environ.get('API_SECRET')

def backtest_rsi():

    starting_fiat_balance = 10000

    trading_fee = 0.001

    TICKER = TickerSymbols.NANOUSDT.name

    # init
    client = Client(api_key, api_secret)

    b_controller = BinanceController(client)

    botcontext = {
        'controller': b_controller,
    }

    # starting date of backtest is set to january 1st 2021
    dt = datetime(2020, 1, 1)
    starting_date = int(dt.replace(tzinfo=timezone.utc).timestamp()) * 1000 # multiply to 1000 for the binance api's weird requirements
    dt2 = datetime(2021, 1, 1)
    ending_date = int(dt2.replace(tzinfo=timezone.utc).timestamp()) * 1000# multiply to 1000 for the binance api's weird requirements
    ending_date = None

    # percentage of portfolio for each trade
    fiat_percent = 1
    coin_percent = 1

    backtest_repository = BacktestRepository(botcontext)

    algolist = [rsi_algo]
    # arguments for algorithms
    algoargs = [[14, 30]]
    # length of each subframe during backtest
    df_search_size = 30

    result = backtest_repository.run_backtest(TICKER, starting_fiat_balance, trading_fee, algolist, algoargs, KlineInterval._1DAY.value, fiat_percent, coin_percent, starting_date, ending_date, df_search_size)
    return result

# function which accepts a dictionary for backtest arguments
def backtest_rsi_external(args):

    TICKER = args["ticker"]
    starting_fiat_balance = args["starting_fiat_balance"]
    starting_coin_balance = args["starting_coin_balance"]

    trading_fee = args["trading_fee"]

    algostringlist = args["algolist"]
    #sort through string list and get function references
    algolist = []
    for algo in algostringlist:
        algolist.append(string_to_reference[algo])
    algoargs = args["algoargs"]

    KlineInterval = args["klineinterval"]

    fiat_percent = args["fiat_percent"]
    coin_percent = args["coin_percent"]

    starting_date = args["starting_date"]
    ending_date = args["ending_date"]

    df_search_size = args["df_search_size"]

    # init
    client = Client(api_key, api_secret)

    b_controller = BinanceController(client)

    botcontext = {
        'controller': b_controller,
    }

    backtest_repository = BacktestRepository(botcontext)

    result = backtest_repository.run_backtest(TICKER, starting_fiat_balance, trading_fee, algolist, algoargs, KlineInterval, fiat_percent, coin_percent, starting_date, ending_date, df_search_size)
    return result

if __name__ == '__main__':
    backtest_rsi()