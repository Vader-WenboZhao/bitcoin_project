import time
import ccxt
import threading
import asyncio

import orderbook_pb2
from Entity import *

latestTradeTimestamp = int(time.time())

'''
Exchanges usually impose what is called a rate limit. A request rate limit in milliseconds.
Specifies the required minimal delay between two consequent HTTP requests to the same exchange.
The built-in rate-limiter is disabled by default and is turned on by setting the enableRateLimit
property to true.

aax fetchOrderBook() limit argument must be None, 20, or 50
bittrex fetchOrderBook() limit argument must be None, 1, 25 or 500, default is 25
'''
exchanges = {1:ccxt.binance(), 2:ccxt.aax(), 3:ccxt.bittrex(), 4:ccxt.bytetrade()}



class GetInfo():
    def __init__(self, exchangeCode, symbol, rateLimit, oderbookCarryFunc, tradesCarryFunc, dbCtrlr):
        global exchanges
        self.exchange = exchanges[exchangeCode]
        self.symbol = symbol # 'BTC/USDT'
        self.exchange.rateLimit = rateLimit
        self.oderbookCarryFunc = oderbookCarryFunc # function to transmit orderbook data
        self.tradesCarryFunc = tradesCarryFunc # function to transmit trades data
        self.exchangeName = self.exchange.name # the name of exchange
        self.databaseControler = dbCtrlr # the object controlling a database
        self.timeCountOrderbook = time.time() # time of the last updating orderbook data
        self.timeCountTrades = time.time() # time of the last updating trades data
        self.lockOrderbook = threading.Lock() # lock of databaseControler's orderbook buffer
        self.lockTrades = threading.Lock() # lock of databaseControler's trades buffer
        # binance = ccxt.binance({'verbose': True, 'rateLimit':10000}) # default rateLimit is 10000

    def getTimestamp(self):
        return self.exchange.fetchTime() # get timestamp from exchange

    async def getOrderbookInfo(self): # 异步操作
        # limit = 5
        while True:
            if time.time() - self.timeCountOrderbook >= 10: # fetch the data once every 2 seconds
                self.timeCountOrderbook = time.time()
                # orderbook = self.exchange.fetchOrderBook(self.symbol, limit) # fetch data
                orderbook = self.exchange.fetchOrderBook(self.symbol) # fetch data
                if orderbook['timestamp'] == None: # the function fetchOrderBook sometimes cannot obtain timestamp
                    timestamp = self.getTimestamp()
                else:
                    timestamp = int(orderbook['timestamp'])
                await self.oderbookCarryFunc(self.exchangeName, self.symbol, orderbook, timestamp, self.databaseControler, self.lockOrderbook)
                print("Got orderbook data!")

    async def getTradesInfo(self): # similar to the above one
        # limit = 5
        while True:
            if time.time() - self.timeCountTrades >= 10:
                self.timeCountTrades = time.time()
                # trades = self.exchange.fetchTrades(self.symbol, limit=limit)
                trades = self.exchange.fetchTrades(self.symbol, since=latestTradeTimestamp)
                await self.tradesCarryFunc(self.exchangeName, self.symbol, trades, self.databaseControler, self.lockTrades)
                print("Got trades data!")


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
]
"""
async def tradesCarryFunction(exchange, symbol, trades, dbControler, lock):
    global latestTradeTimestamp

    tradesToSave = orderbook_pb2.TradesInfo() # initiate an orderbook_pb2.TradesInfo object

    for trade in trades:
        newTrade = tradesToSave.trades.add() # repeated data type

        newTrade.exchange = exchange # assignment
        newTrade.symbol = symbol
        newTrade.timestamp = trade['timestamp']
        newTrade.datetime = trade['datetime']
        newTrade.side = trade['side']
        newTrade.price = trade['price']
        newTrade.amount = trade['amount']

        if trade['timestamp'] > latestTradeTimestamp: # give this value to 'since'
            latestTradeTimestamp = trade['timestamp']

    byteStream = tradesToSave.SerializeToString() # serialization

    lock.acquire() # thread lock
    dbControler.tradesBuffer.append(byteStream) # append the serialized data to databaseControler's buffer
    lock.release()

    print("Add trades to buffer successfully!")

    return


"""
{'bids': [ [54785.31, 0.000365], [54785.3, 0.128567], [54784.4, 0.105001], [54784.39, 0.5], [54781.68, 0.463525], [54781.67, 0.01503], [54780.72, 0.6], [54780.7, 0.004], [54778.5, 0.004672], [54778.31, 0.057] ],
'asks': [ [54793.82, 0.5], [54794.48, 0.000364], [54794.49, 0.1274], [54795.45, 0.5], [54795.46, 1.2], [54796.83, 0.0075], [54797.82, 0.022272], [54799.71, 0.252369], [54799.76, 0.5], [54799.77, 0.003869] ],
'timestamp': None, 'datetime': None, 'nonce': 10166925112}
"""
async def oderbookCarryFunction(exchange, symbol, orderbook, timestamp, dbControler, lock): # similar to the above function
    orderBookToSave = orderbook_pb2.Orderbook()

    orderBookToSave.exchange = exchange
    orderBookToSave.symbol = symbol
    orderBookToSave.timestamp = timestamp

    for bid in orderbook['bids']:
        # bid is a list with two floats [price, amount]: [54785.31, 0.000365]
        newBid = orderBookToSave.bids.bidUnits.add()
        newBid.price = bid[0]
        newBid.amount = bid[1]
    for ask in orderbook['asks']:
        # ask is a list with two floats [price, amount]: [54793.82, 0.5]
        newAsk = orderBookToSave.asks.askUnits.add()
        newAsk.price = ask[0]
        newAsk.amount = ask[1]

    # print(orderBookToSave)
    byteStream = orderBookToSave.SerializeToString()

    lock.acquire()
    dbControler.orderBookBuffer.append(byteStream)
    lock.release()

    print("Add orderbook to buffer successfully!")

    return


class DatabaseOperatorOrderBook(threading.Thread): # the thread inserting orderbook data to database
    def __init__(self, dbControler):
        threading.Thread.__init__(self)
        self.databaseControler = dbControler

    def run(self):
        self.databaseControler.insertOrderbookData()


class DatabaseOperatorTrades(threading.Thread): # the thread inserting trades data to database
    def __init__(self, dbControler):
        threading.Thread.__init__(self)
        self.databaseControler = dbControler

    def run(self):
        self.databaseControler.insertTradesData()


class ThreadGetTradesInfo(threading.Thread): # the thread collecting trades data
    def __init__(self, getInfoObject):
        threading.Thread.__init__(self)
        self.object = getInfoObject

    def run(self):
        print('Thread GetTradesInfo starts')
        loop1 =  asyncio.new_event_loop() # async
        asyncio.set_event_loop(loop1)
        res = loop1.run_until_complete(asyncio.wait([self.object.getTradesInfo()]))
        loop1.close() # in fact it will never close

class ThreadGetOrderBookInfo(threading.Thread): # the thread collecting orderbook data
    def __init__(self, getInfoObject):
        threading.Thread.__init__(self)
        self.object = getInfoObject

    def run(self): # similar to the above one
        print('Thread GetOrderBookInfo starts')
        loop2 =  asyncio.new_event_loop()
        asyncio.set_event_loop(loop2)
        res = loop2.run_until_complete(asyncio.wait([self.object.getOrderbookInfo()]))
        loop2.close()


def operateExchange(dbControler, exchangeNum, symbol, rateLimit): # specific to a certain exchange
    getBinanceInfo = GetInfo(exchangeNum, symbol, rateLimit, oderbookCarryFunction, tradesCarryFunction, dbControler) # the object to collect orderbook and trades data

    dbOperatorOrderBook = DatabaseOperatorOrderBook(dbControler)
    dbOperatorOrderBook.start()
    dbOperatorTrades = DatabaseOperatorTrades(dbControler)
    dbOperatorTrades.start()
    threadGetTradesInfo = ThreadGetTradesInfo(getBinanceInfo)
    threadGetTradesInfo.start()
    threadGetOrderBookInfo = ThreadGetOrderBookInfo(getBinanceInfo)
    threadGetOrderBookInfo.start()



if __name__ == "__main__":

    DBCtrlr = DatabaseControler() # object responsible for operating the database

    operateExchange(DBCtrlr, 1, 'BTC/USDT', 2000)

    operateExchange(DBCtrlr, 2, 'BTC/USDT', 500)

    # operateExchange(DBCtrlr, 3, 'BTC/USDT', 1500)

    operateExchange(DBCtrlr, 4, 'BTC/USDT', 500)

    DBCtrlr.bufferMonitor()
