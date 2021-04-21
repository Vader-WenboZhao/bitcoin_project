import time
import ccxt
import threading
# import asyncio

import orderbook_pb2
from Entity import *

exchanges = {1:ccxt.binance()}

# buffer = []

DBCtrlr = DatabaseControler()

# loop = asyncio.get_event_loop()

class GetInfo(): # symbol = 'BTC/USDT'
    def __init__(self, exchangeCode, symbol, rateLimit, orderBookCarryFunc, tradesCarryFunc):
        global exchanges
        self.exchange = exchanges[exchangeCode]
        self.symbol = symbol
        self.exchange.rateLimit = rateLimit
        self.orderBookCarryFunc = orderBookCarryFunc
        self.tradesCarryFunc = tradesCarryFunc
        self.exchangeName = self.exchange.name
        # binance = ccxt.binance({'verbose': True, 'rateLimit':10000}) # default rateLimit is 10000

    def getTimestamp(self):
        return self.exchange.fetchTime()

    def getOrderbookInfo(self):
        limit = 5
        while True:
            orderbook = self.exchange.fetchOrderBook(self.symbol, limit=limit)
            timestamp = self.getTimestamp()
            # print(orderbook)
            self.orderBookCarryFunc(self.exchangeName, self.symbol, orderbook, timestamp)
            time.sleep(2)

    def getTradesInfo(self):
        limit = 5
        while True:
            trades = self.exchange.fetchTrades(self.symbol, limit=limit)
            self.tradesCarryFunc(self.exchangeName, self.symbol, trades)
            time.sleep(2)


"""
[
    {
    'info':
        {
        'a': '696891019',
        'p': '55465.93000000',
        'q': '0.00182700',
        'f': '782107950',
        'l': '782107950',
        'T': '1618995478345',
        'm': False,
        'M': True
        },
    'timestamp': 1618995478345,
    'datetime': '2021-04-21T08:57:58.345Z',
    'symbol': 'BTC/USDT',
    'id': '696891019',
    'order': None,
    'type': None,
    'side': 'buy', # 'buy' OR 'sell'
    'takerOrMaker': None,
    'price': 55465.93,
    'amount': 0.001827,
    'cost': 101.33625411,
    'fee': None
    },
    ...
    {'info': {'a': '696891020', 'p': '55465.93000000', 'q': '0.12246400', 'f': '782107951', 'l': '782107951', 'T': '1618995478431', 'm': False, 'M': True}, 'timestamp': 1618995478431, 'datetime': '2021-04-21T08:57:58.431Z', 'symbol': 'BTC/USDT', 'id': '696891020', 'order': None, 'type': None, 'side': 'buy', 'takerOrMaker': None, 'price': 55465.93, 'amount': 0.122464, 'cost': 6792.57965152, 'fee': None}, {'info': {'a': '696891021', 'p': '55465.93000000', 'q': '0.01442300', 'f': '782107952', 'l': '782107952', 'T': '1618995478695', 'm': False, 'M': True}, 'timestamp': 1618995478695, 'datetime': '2021-04-21T08:57:58.695Z', 'symbol': 'BTC/USDT', 'id': '696891021', 'order': None, 'type': None, 'side': 'buy', 'takerOrMaker': None, 'price': 55465.93, 'amount': 0.014423, 'cost': 799.98510839, 'fee': None}
]
"""

def tradesCarryFunction(exchange, symbol, trades):
    global DBCtrlr

    tradesToSave = orderbook_pb2.TradesInfo()

    for trade in trades:
        newTrade = tradesToSave.trades.add()

        newTrade.exchange = exchange
        newTrade.symbol = symbol
        newTrade.timestamp = trade['timestamp']
        newTrade.datetime = trade['datetime']
        newTrade.side = trade['side']
        newTrade.price = trade['price']
        newTrade.amount = trade['amount']

    byteStream = tradesToSave.SerializeToString()

    return DBCtrlr.insertTradesData(byteStream)


"""
{
    'bids': [
        [54785.31, 0.000365], [54785.3, 0.128567], ... [54778.31, 0.057]
    ],
    'asks': [
        [54793.82, 0.5], [54794.48, 0.000364], ... [54799.77, 0.003869]
    ],
    'timestamp': None,
    'datetime': None,
    'nonce': 10166925112}
"""

def oderbookCarryFunction(exchange, symbol, orderbook, timestamp):
    global DBCtrlr

    orderBookToSave = orderbook_pb2.Orderbook()
    orderBookToSave.exchange = exchange
    orderBookToSave.symbol = symbol
    orderBookToSave.nonce = orderbook['nonce']
    orderBookToSave.timestamp = timestamp

    for bid in orderbook['bids']:
        # bid is a list with two floats: [54785.31, 0.000365]
        newBid = orderBookToSave.bids.bidUnits.add()
        newBid.price = bid[0]
        newBid.amount = bid[1]
    for ask in orderbook['asks']:
        # ask is a list with two floats: [54793.82, 0.5]
        newAsk = orderBookToSave.asks.askUnits.add()
        newAsk.price = ask[0]
        newAsk.amount = ask[1]

    # print(orderBookToSave)
    # print(orderBookToSave.SerializeToString())
    # print(orderBookToSave)
    byteStream = orderBookToSave.SerializeToString()
    # print(orderBookToSave.ParseFromString(byteStream))

    return DBCtrlr.insertOrderbookData(byteStream)


class ThreadOrderbook(threading.Thread):
    def __init__(self, getInfoObject):
        threading.Thread.__init__(self)
        self.object = getInfoObject

    def run(self):
        try:
            self.object.getOrderbookInfo()
        except BaseException as e:
            print("Error in ThreadOrderbook.run(): ", e)


class ThreadTrades(threading.Thread):
    def __init__(self, getInfoObject):
        threading.Thread.__init__(self)
        self.object = getInfoObject

    def run(self):
        self.object.getTradesInfo()



if __name__ == "__main__":
    getBinanceInfo = GetInfo(1, 'BTC/USDT', 10000, oderbookCarryFunction, tradesCarryFunction)

    threadBinanceOrderbook = ThreadOrderbook(getBinanceInfo)
    threadBinanceOrderbook.start()
    print("Thread to collect Binance orderbook starts now!")
    
    threadBinanceTrades = ThreadTrades(getBinanceInfo)
    threadBinanceTrades.start()
    print("Thread to collect Binance trades starts now!")
