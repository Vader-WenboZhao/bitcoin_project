import time
import ccxt
import threading
import asyncio

import orderbook_pb2
from Entity import *

exchanges = {1:ccxt.binance()}

oderBookBuffer = []
tradesBuffer = []

DBCtrlr = DatabaseControler()


class GetInfo(): # symbol = 'BTC/USDT'
    def __init__(self, exchangeCode, symbol, rateLimit, oderbookCarryFunc, tradesCarryFunc):
        global exchanges
        self.exchange = exchanges[exchangeCode]
        self.symbol = symbol
        self.exchange.rateLimit = rateLimit
        self.oderbookCarryFunc = oderbookCarryFunc
        self.tradesCarryFunc = tradesCarryFunc
        self.exchangeName = self.exchange.name
        # binance = ccxt.binance({'verbose': True, 'rateLimit':10000}) # default rateLimit is 10000

    def getTimestamp(self):
        return self.exchange.fetchTime()

    async def getOrderbookInfo(self): # 异步操作
        limit = 5
        while True:
            orderbook = self.exchange.fetchOrderBook(self.symbol, limit)
            timestamp = self.getTimestamp()
            # print(orderbook)
            await self.oderbookCarryFunc(self.exchangeName, self.symbol, orderbook, timestamp)
            time.sleep(2)

    async def getTradesInfo(self):
        limit = 5
        while True:
            trades = self.exchange.fetchTrades(self.symbol, limit=limit)
            await self.tradesCarryFunc(self.exchangeName, self.symbol, trades)
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
    'side': 'buy',
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

async def tradesCarryFunction(exchange, symbol, trades):
    global DBCtrlr
    global tradesBuffer

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

    tradesBuffer.append(byteStream)

    return


"""
{'bids': [ [54785.31, 0.000365], [54785.3, 0.128567], [54784.4, 0.105001], [54784.39, 0.5], [54781.68, 0.463525], [54781.67, 0.01503], [54780.72, 0.6], [54780.7, 0.004], [54778.5, 0.004672], [54778.31, 0.057] ],
'asks': [ [54793.82, 0.5], [54794.48, 0.000364], [54794.49, 0.1274], [54795.45, 0.5], [54795.46, 1.2], [54796.83, 0.0075], [54797.82, 0.022272], [54799.71, 0.252369], [54799.76, 0.5], [54799.77, 0.003869] ],
'timestamp': None, 'datetime': None, 'nonce': 10166925112}
"""
async def oderbookCarryFunction(exchange, symbol, orderbook, timestamp):
    global DBCtrlr
    global oderBookBuffer

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
    byteStream = orderBookToSave.SerializeToString()

    oderBookBuffer.append(byteStream)

    return


class DatabaseOperatorOrderBook(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global oderBookBuffer

        while True:
            if len(oderBookBuffer)!=0:
                byteStream = oderBookBuffer.pop(0)
                DBCtrlr.insertOrderbookData(byteStream)
            else:
                time.sleep(0.05)
                continue


class DatabaseOperatorTrades(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global tradesBuffer

        while True:
            if len(tradesBuffer)!=0:
                byteStream = tradesBuffer.pop(0)
                DBCtrlr.insertTradesData(byteStream)
            else:
                time.sleep(0.05)
                continue


class ThreadGetTradesInfo(threading.Thread):
    def __init__(self, getInfoObject):
        threading.Thread.__init__(self)
        self.object = getInfoObject

    def run(self):
        loop1 =  asyncio.new_event_loop()
        asyncio.set_event_loop(loop1)
        res = loop1.run_until_complete(asyncio.wait([self.object.getTradesInfo()]))
        loop1.close()

class ThreadGetOrderBookInfo(threading.Thread):
    def __init__(self, getInfoObject):
        threading.Thread.__init__(self)
        self.object = getInfoObject

    def run(self):
        loop2 =  asyncio.new_event_loop()
        asyncio.set_event_loop(loop2)
        res = loop2.run_until_complete(asyncio.wait([self.object.getOrderbookInfo()]))
        loop2.close()


if __name__ == "__main__":

    dbOperatorOrderBook = DatabaseOperatorOrderBook()
    dbOperatorOrderBook.start()

    dbOperatorTrades = DatabaseOperatorTrades()
    dbOperatorTrades.start()

    getBinanceInfo = GetInfo(1, 'BTC/USDT', 10000, oderbookCarryFunction, tradesCarryFunction)

    threadGetTradesInfo = ThreadGetTradesInfo(getBinanceInfo)
    threadGetTradesInfo.start()

    threadGetOrderBookInfo = ThreadGetOrderBookInfo(getBinanceInfo)
    threadGetOrderBookInfo.start()
