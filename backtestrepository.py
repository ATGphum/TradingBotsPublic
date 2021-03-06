from binancecontroller import BinanceController
from enums import *
from datetime import datetime
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

        win_trades = 0
        lose_trades = 0
        last_balance = fiat_balance # comparatpr used to determine if a trade was won in terms of fiat
        winning_rate = 0
        remainder_after_trade = 1 - trading_fee
        coin_worth = 0

        while top_index <= len(globalframe.index):
            # get current window dataframe
            focus_frame = globalframe.iloc[bottom_index : top_index]
            coin_price = float(focus_frame['close'].iloc[-1])
            current_unixtime = float(focus_frame.index[-1]) / 1000

            # add the focus frame to each list in algo arguments list     
            temp_algo_args = list(map(lambda args: [focus_frame] + args, algo_args.copy()))
            algo_response = self.check_all_algos(algo_list, temp_algo_args)

       
            if algo_response == AlgoResponse.BUY and bought == 0:
                last_balance = fiat_balance # store the current fiat balance for comparison for win/loss
                coin_balance = coin_balance + ((fiat_balance * fiat_percent) / coin_price) * remainder_after_trade 
                fiat_balance = fiat_balance - (fiat_balance * fiat_percent)
                bought = 1

            if algo_response == AlgoResponse.SELL and bought == 1:
                fiat_balance = fiat_balance + ((coin_balance * coin_percent) * coin_price) * remainder_after_trade
                coin_balance = coin_balance - (coin_balance * coin_percent)
                bought = 0

                if fiat_balance > last_balance:
                    win_trades = win_trades + 1
                elif fiat_balance < last_balance:
                    lose_trades = lose_trades + 1

            print("simulating {}".format(self.unix_to_readable_date(current_unixtime)))
            print("fiat balance is ${}".format(fiat_balance))
            coin_worth = round(coin_balance * coin_price, 2)
            print("coin balance is {} worth ${}".format(coin_balance, coin_worth))
            if win_trades + lose_trades != 0:
                winning_rate = round((win_trades/(win_trades + lose_trades)) * 100, 2)
                print("win rate is {}%".format(winning_rate))
            top_index = top_index + 1
            bottom_index = bottom_index + 1
        return (fiat_balance, coin_balance, coin_worth, winning_rate)

    def unix_to_readable_date(self, unixtime):
        timestamp = datetime.fromtimestamp(unixtime)
        return timestamp.strftime('%Y-%m-%d %H:%M:%S')

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
        coin_df.to_csv('{}_bars3.csv'.format(ticker_symbol))

        return coin_df


