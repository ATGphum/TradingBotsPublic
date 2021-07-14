import talibrary
import math
from enums import *

def rsi_algo(df, period=14, cutoff=30):
    rsi = talibrary.calculate_rsi(df, period).iloc[-1]
    if math.isnan(rsi):
        return AlgoResponse.IGNORE
    elif rsi > 100 - cutoff:
        return AlgoResponse.SELL
    elif rsi < cutoff:
        return AlgoResponse.BUY
    else:
        return AlgoResponse.IGNORE

def sma_algo(df, period=14, cutoff=45):
    rsi = talibrary.calculate_rsi(df, period).iloc[-1]
    if math.isnan(rsi):
        return AlgoResponse.IGNORE
    elif rsi > 100 - cutoff:
        return AlgoResponse.SELL
    elif rsi < cutoff:
        return AlgoResponse.BUY
    else:
        return AlgoResponse.IGNORE

def ema_algo(df, period=14, cutoff=37):
    rsi = talibrary.calculate_rsi(df, period).iloc[-1]
    if math.isnan(rsi):
        return AlgoResponse.IGNORE
    elif rsi > 100 - cutoff:
        return AlgoResponse.SELL
    elif rsi < cutoff:
        return AlgoResponse.BUY
    else:
        return AlgoResponse.IGNORE

# returns a reference to each algo function when given the name in string
string_to_reference = {
    "rsi_algo": rsi_algo,
    "sma_algo": sma_algo,
    "ema_algo": ema_algo
}