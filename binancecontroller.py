from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
from binance.websockets import BinanceSocketManager
from twisted.internet import reactor
import sys


class BinanceController:

    def __init__(self, client):
        try:
            self.client = client
            self.bsm = BinanceSocketManager(self.client)
            print('successfully created BinanceController object')
        except:
            print('failed to initialise BinanceController object')

    # gets ticker symbol information and returns message to supplied callback function
    def get_ticker_socket_callback(self, ticker_symbol, call_back_function):
        try:
            conn_key = self.bsm.start_symbol_ticker_socket(
                ticker_symbol, call_back_function)
            print('successfully initialised ticker socket callback')
        except:
            print('failed to initialize ')

    # starts binance web socket
    def start_socket(self):
        try:
            self.bsm.start()
            print('successfully started binance socket')
        except :
            print('failed to start binance socket')

    # stops socket on given connection key
    def stop_socket(self, conn_key):
        try:
            self.bsm.stop_socket(conn_key)
            reactor.stop()
            print('successfully stopped binance socket')
        except:
            print('failed to stop binance socket')

    # get historical klines from binance
    def retrieve_historical_data(self, ticker_symbol, interval, earliest_time, latest_time, num_limit):
        # valid intervals - 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
        try:
            if latest_time is not None:
                data = self.client.get_historical_klines(ticker_symbol, interval, earliest_time, end_str=latest_time, limit=num_limit)
            else:
                data = self.client.get_historical_klines(ticker_symbol, interval, earliest_time, limit=num_limit)
            print('succesfully retrieved historical data')
            return data
        except BinanceAPIException as e:
            print(e)
            print('failed to retrieve historical data')
        except:
            print('failed to retrieve historical data')

    # fire an order to binance
    def fire_order(self, ticker_symbol, order_side, order_type, time_in_force, order_quantity, order_price):
        try:
            order = self.client.create_test_order(
                symbol=ticker_symbol,
                side=order_side,
                type=order_type,
                timeInForce=time_in_force,
                quantity=order_quantity,
                price=order_price
            )
            return 1
        except BinanceAPIException as e:
            print(e)
            return 0
        except BinanceOrderException as e:
            print(e)
            return 0
        except:
            print('failed to fire order')
            print(sys.exc_info()[0])
            return 0