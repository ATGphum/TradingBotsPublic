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
    
    