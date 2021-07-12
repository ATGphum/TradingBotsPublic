import enum

class TickerSymbols(enum.Enum):
    DOTUSDT = 1
    NANOUSDT = 2
    ADAUSDT = 3
    USDCUSDT = 4
    BTCUSDT = 5
    ETHUSDT = 6

class OrderStatus(enum.Enum):
    NEW = 1
    PARTIALLY_FILLED = 2
    FILLED = 3 
    CANCELED = 4
    PENDING_CANCEL = 5
    REJECTED = 6
    EXPIRED = 7

class KlineInterval(enum.Enum):
    _1MINUTE = '1m'
    _3MINUTE = '3m'
    _5MINUTE = '5m'
    _15MINUTE = '15m'
    _30MINUTE = '30m'
    _1HOUR = '1h'
    _2HOUR = '2h'
    _4HOUR = '4h'
    _6HOUR = '6h'
    _8HOUR = '8h'
    _12HOUR = '12h'
    _1DAY = '1d'
    _3DAY = '3d'
    _1WEEK = '1w'
    _1MONTH = '1M'

class OrderSide(enum.Enum):
    BUY = 1
    SELL = 2

class OrderType(enum.Enum):
    LIMIT = 1 
    MARKET = 2
    STOP_LOSS = 3 
    STOP_LOSS_LIMIT = 4
    TAKE_PROFIT = 5
    TAKE_PROFIT_LIMIT = 6
    LIMIT_MAKER = 7

class TimeinForce(enum.Enum):
    GTC = 1
    IOC = 2
    FOK = 3
    GTX = 4

class OrderResponse(enum.Enum):
    ACK = 1
    RESULT = 2
    FULL = 3

class WebsocketDepth(enum.Enum):
    five = 5
    ten = 10
    twenty = 20

class AlgoResponse(enum.Enum):
    BUY = 1
    SELL = 2
    IGNORE = 3