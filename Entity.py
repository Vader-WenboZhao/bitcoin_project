import django
from django.db import models
from django.conf import settings
from django.db import connection
import orderbook_pb2
import collections
import copy
import threading


# Django Database

INSTALLED_APPS = [
    "Entity"
]



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # mysql
        'NAME': 'coin', # database name
        'USER': 'root', # user name
        'PASSWORD': 'zhaowenbo2305', # password
        'HOST': '127.0.0.1', # default
        'PORT': '3306', # default
    }
}


settings.configure(DATABASES=DATABASES, INSTALLED_APPS=INSTALLED_APPS)

django.setup()



'''
cursor = connection.cursor()
cursor.execute("create database coindata")
cursor.execute("show databases")
rows = cursor.fetchall()
for row in rows:
    print(row)
'''


# CREATE TABLE orderbook ( exchange VARCHAR(20), symbol VARCHAR(10), nonce BIGINT, timestamp BIGINT, type VARCHAR(3), price DOUBLE, amount DOUBLE);
# CREATE TABLE trades ( exchange VARCHAR(20), symbol VARCHAR(10), timestamp BIGINT, datetime VARCHAR(30), side VARCHAR(4), price DOUBLE, amount DOUBLE);

class Orderbook(models.Model):
    # exchange = models.TextField(db_column=u'exchange', primary_key=True)
    exchange = models.TextField(db_column=u'exchange')
    symbol = models.TextField(db_column=u'symbol')
    nonce = models.TextField(db_column=u'nonce')
    timestamp = models.TextField(db_column=u'timestamp')
    type = models.TextField(db_column=u'timestamp') # 'bid' OR 'ask'
    price = models.TextField(db_column=u'price')
    amount = models.TextField(db_column=u'amount')

    def __unicode__(self):
        return 'orderbook'
    # table_name
    class Meta:
        db_table = 'orderbook'


class DatabaseControler(): # class operating on the mysql database
    def __init__(self):
        self.orderBookBuffer = collections.deque([]) # a FIFO queue
        self.tradesBuffer = collections.deque([]) # a FIFO queue
        self.lockOrderbook = threading.Lock() # thread lock for orderbook buffer
        self.lockTrades = threading.Lock() # thread lock for trades buffer

    def insertOrderbookData(self): # insert orderbook data to database
        print("Thread insertOrderbookData starts")
        while True:
            if len(self.orderBookBuffer) != 0: # check and monitor the buffer
                self.lockOrderbook.acquire() # thread lock
                byteStream = copy.deepcopy(self.orderBookBuffer.popleft()) # deepcopy data from buffer
                self.lockOrderbook.release()

                orderBookTool = orderbook_pb2.Orderbook() # used to parse info from the byte stream
                orderBookTool.ParseFromString(byteStream)

                exchangeName = orderBookTool.exchange # parse info from byte stream
                symbol = orderBookTool.symbol
                nonce = orderBookTool.nonce
                timestamp = orderBookTool.timestamp

                cursor = connection.cursor() # get the cursor

                try:
                    for bid in orderBookTool.bids.bidUnits: # insert bid data to database table
                        cursor.execute("insert into orderbook values(\'"+exchangeName+"\',\'"+symbol+"\',"+str(nonce)+","+str(timestamp)+",\'bid\',"+str(bid.price)+","+str(bid.amount)+")")

                    for ask in orderBookTool.asks.askUnits: # insert ask data to database table
                        cursor.execute("insert into orderbook values(\'"+exchangeName+"\',\'"+symbol+"\',"+str(nonce)+","+str(timestamp)+",\'ask\',"+str(ask.price)+","+str(ask.amount)+")")
                except BaseException as e:
                    print("* * * * * * * * * * Error! * * * * * * * * * *\n", e)
                    continue

                continue

            else:
                continue



    def insertTradesData(self): # insert trades data to database, similar to the above one
        print("Thread insertTradesData starts")
        while True:
            if len(self.tradesBuffer) != 0:
                self.lockTrades.acquire()
                byteStream = copy.deepcopy(self.tradesBuffer.popleft()) # deep copy
                self.lockTrades.release()

                tradesTool = orderbook_pb2.TradesInfo()
                tradesTool.ParseFromString(byteStream)

                cursor = connection.cursor()

                try:
                    for trade in tradesTool.trades:
                        cursor.execute("insert into trades values(\'"+trade.exchange+"\',\'"+trade.symbol+"\',"+str(trade.timestamp)+",\'"+trade.datetime+"\',\'"+trade.side+"\',"+str(trade.price)+","+str(trade.amount)+")")
                except BaseException as e:
                    print("* * * * * * * * * * Error! * * * * * * * * * *\n", e)
                    continue

                continue

            else:
                continue
