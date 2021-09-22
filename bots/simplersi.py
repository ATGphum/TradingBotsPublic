import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from analysisrepository import AnalysisRepository
from binancecontroller import BinanceController
from twisted.internet import reactor
from binance.websockets import BinanceSocketManager
from binance.client import Client
from enums import *
import time
import schedule
import btalib

#init environ variables
api_key = os.environ.get('API_KEY')
api_secret = os.environ.get('API_SECRET')

def simple_rsi():

    TICKER = TickerSymbols.NANOUSDT.name

    klineInterval = KlineInterval._1HOUR.value

    # init
    client = Client(api_key, api_secret)

    b_controller = BinanceController(client)

    botcontext = {
        'controller': b_controller,
        'bought': 0,
        'last_data_frame': None
    }

    analysis_repository = AnalysisRepository(botcontext)

    schedule.every(10).seconds.do(analysis_repository.run_simple_rsi, TICKER, klineInterval)

    while True:
        schedule.run_pending()
        time.sleep(1)