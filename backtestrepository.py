from binancecontroller import BinanceController
from enums import *
import functools
import time
import pandas as pd
import btalib
import talibrary
import algocollection

class BacktestRepository:
    def __init__(self, context):
        self.context = context

    # ticker symbol for coin in question
    # algo_list is list of references to algorithm functions to determine whether to buy or sell
    # algo_args contains arguments corresponding to the aformentioned functions
    # begin_date is time in UTC
    def run_backtest(self, ticker, starting_fiat_balance, trading_fee, algo_list, algo_args, interval, fiat_percent, coin_percent, begin_date, end_date, df_search_size):
        # retrieve candle dataframe from beginning date
        globalframe = self.retrieve_and_clean_data(ticker, interval, begin_date, end_date, 1000)
        top_index = df_search_size
        bottom_index = 0

        fiat_balance = starting_fiat_balance
        coin_balance = 0
        bought = 0

        while top_index <= len(globalframe.index):
            # get current window dataframe
            focus_frame = globalframe.iloc[bottom_index : top_index]
            coin_price = float(focus_frame['close'].iloc[-1])

            # add the focus frame to each list in algo arguments list     
            temp_algo_args = list(map(lambda args: [focus_frame] + args, algo_args.copy()))
            algo_response = self.check_all_algos(algo_list, temp_algo_args)
       
            if algo_response == AlgoResponse.BUY and bought == 0:
                coin_balance = coin_balance + ((fiat_balance * fiat_percent) / coin_price) * trading_fee 
                fiat_balance = fiat_balance - (fiat_balance * fiat_percent)
                bought = 1

            if algo_response == AlgoResponse.SELL and bought == 1:
                fiat_balance = fiat_balance + ((coin_balance * coin_percent) * coin_price) * trading_fee
                coin_balance = coin_balance - (coin_balance * coin_percent)
                bought = 0

            print("fiat balance is ${}".format(fiat_balance))
            print("coin balance is {} worth {}".format(coin_balance, coin_balance * coin_price))
            top_index = top_index + 1
            bottom_index = bottom_index + 1

    # returns buy enum if all algos returns an order to buy, otherwise returns sell enum if all algos returns an order to sell, otherwise returns ignore
    def check_all_algos(self, algo_list, algo_args):

        algo_results = []

        for i in range(0, len(algo_list)):
            algo_result = algo_list[i](*algo_args[i])
            algo_results.append(algo_result)

        if AlgoResponse.SELL not in algo_results and AlgoResponse.IGNORE not in algo_results:
            return AlgoResponse.BUY
        elif AlgoResponse.BUY not in algo_results and AlgoResponse.IGNORE not in algo_results:
            return AlgoResponse.SELL
        else:
            return AlgoResponse.IGNORE
    
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


