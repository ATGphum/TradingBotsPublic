from binancecontroller import BinanceController
from enums import *
import time
import pandas as pd
import btalib
import talibrary

class AnalysisRepository:
    def __init__(self, context):
        self.context = context 

    def run_simple_rsi(self, ticker_symbol):
        interval = KlineInterval._1HOUR.value
        timeframe = int((time.time() - (7 * 3 * 60 * 60)) * 1000)

        # retrieve dataframe
        self.context["last_data_frame"] = self.retrieve_and_clean_data(ticker_symbol, interval, timeframe, None, 500)

        rsi = self.get_rsi()
        print("{} rsi is {}".format(interval, rsi))

        price = self.get_current_price()
        print("current price is {}".format(price))

        # if bought and rsi over 0.7, sell
        if rsi > 70 and self.context['bought'] == 1:
            success = self.make_order(ticker_symbol, OrderSide.SELL.name, OrderType.LIMIT.name, TimeinForce.GTC.name, 200, 100)
            if success:
                self.context['bought'] = 0

        # if not yet bought and rsi under 0.3, buy
        elif rsi < 30 and self.context['bought'] == 0:
            success = self.make_order(ticker_symbol, OrderSide.BUY.name, OrderType.LIMIT.name, TimeinForce.GTC.name, 200, 100)
            if success:
                self.context['bought'] = 1

        print("Bought state is {}".format(self.context['bought']))

    def make_order(self, ticker_symbol, order_side, order_type, time_in_force, order_quantity, order_price):
        status =  self.context['controller'].fire_order(ticker_symbol, order_side, order_type, time_in_force, order_quantity, order_price)
        print("succesfully placed {} {} order for {} {} at ${}".format(order_side, order_type, order_quantity, ticker_symbol, order_price))
        return status

    # gets the rsi using the dataframe stored in context object
    def get_rsi(self):

        coin_df = self.context['last_data_frame']
        temp = talibrary.calculate_rsi(coin_df)
        # print(temp)
        return temp.iloc[-1]

    def get_current_price(self):
        coin_df = self.context['last_data_frame']
        return coin_df['close'].iloc[-1]
    
    def retrieve_and_clean_data(self, ticker_symbol, interval, fromdate, todate, num_limit):

        bars = self.context['controller'].retrieve_historical_data(
            ticker_symbol, interval, fromdate, todate, num_limit)

        # delete unwanted data - just keep date, open, high, low, close
        for line in bars:
            del line[5:]
        # create a Pandas DataFrame and export to CSV
        coin_df = pd.DataFrame(
            bars, columns=['date', 'open', 'high', 'low', 'close'])
        coin_df.set_index('date', inplace=True)

        # export DataFrame to csv
        # coin_df.to_csv('{}_bars3.csv'.format(ticker_symbol))

        return coin_df

    