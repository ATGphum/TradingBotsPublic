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

#init environ variables
api_key = os.environ.get('API_KEY')
api_secret = os.environ.get('API_SECRET')

def main():

    starting_fiat_balance = 1000

    trading_fee = 0.999

    TICKER = TickerSymbols.DOTUSDT.name

    # init
    client = Client(api_key, api_secret)

    b_controller = BinanceController(client)

    botcontext = {
        'controller': b_controller,
    }

    # starting date of backtest is set to january 1st 2021
    dt = datetime(2021, 1, 1)
    starting_date = int(dt.replace(tzinfo=timezone.utc).timestamp()) * 1000 # multiply to 1000 for the binance api's weird requirements
    #datetime(2021, 1, 1)
    #ending_date = int(dt.replace(tzinfo=timezone.utc).timestamp()) * 1000 # multiply to 1000 for the binance api's weird requirements
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

    backtest_repository.run_backtest(TICKER, starting_fiat_balance, trading_fee, algolist, algoargs, KlineInterval._1HOUR.value, fiat_percent, coin_percent, starting_date, ending_date, df_search_size)

if __name__ == '__main__':
    main()