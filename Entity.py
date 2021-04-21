import django
from django.db import models
from django.conf import settings
from django.db import connection
import orderbook_pb2



INSTALLED_APPS = [
    "Entity"
]



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        # 数据库名
        'NAME': 'coin',
        'USER': 'root',
        'PASSWORD': 'zhaowenbo2305',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}


settings.configure(DATABASES=DATABASES, INSTALLED_APPS=INSTALLED_APPS)

django.setup()



'''
# 获取游标对象
cursor = connection.cursor()
# 拿到游标对象后执行sql语句
cursor.execute("select * from book")
# 获取所有的数据
rows = cursor.fetchall()
# 遍历查询到的数据
for row in rows:
    print(row)
'''

'''
cursor = connection.cursor()
cursor.execute("create database coindata")
cursor.execute("show databases")
rows = cursor.fetchall()
for row in rows:
    print(row)
'''


# CREATE TABLE orderbook ( exchange VARCHAR(20), symbol VARCHAR(10), nonce BIGINT,
# timestamp BIGINT, type VARCHAR(3), price DOUBLE, amount DOUBLE,
# PRIMARY KEY(exchange, symbol, timestamp, type) );

class Orderbook(models.Model):

    '''
    exchange = models.TextField(db_column=u'exchange', primary_key=True)
    symbol = models.TextField(db_column=u'symbol', primary_key=True)
    nonce = models.TextField(db_column=u'nonce', primary_key=True)
    timestamp = models.TextField(db_column=u'timestamp', primary_key=True)
    type = models.TextField(db_column=u'timestamp', primary_key=True) # 'bid' OR 'ask'
    price = models.TextField(db_column=u'price')
    amount = models.TextField(db_column=u'amount')
    '''

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


class DatabaseControler():
    def __init__(self):
        pass

    # byteStream:

    def insertOrderbookData(self, byteStream):
        orderBookTool = orderbook_pb2.Orderbook()
        orderBookTool.ParseFromString(byteStream)

        exchangeName = orderBookTool.exchange
        symbol = orderBookTool.symbol
        nonce = orderBookTool.nonce
        timestamp = orderBookTool.timestamp

        cursor = connection.cursor()

        try:
            for bid in orderBookTool.bids.bidUnits:
                cursor.execute("insert into orderbook values(\'"+exchangeName+"\',\'"+symbol+"\',"+str(nonce)+","+str(timestamp)+",\'bid\',"+str(bid.price)+","+str(bid.amount)+")")

            for ask in orderBookTool.asks.askUnits:
                cursor.execute("insert into orderbook values(\'"+exchangeName+"\',\'"+symbol+"\',"+str(nonce)+","+str(timestamp)+",\'ask\',"+str(ask.price)+","+str(ask.amount)+")")
        except BaseException as e:
            print("* * * * * * * * * * Error! * * * * * * * * * *\n", e)
            return False

        return True

    def insertTradesData(self, byteStream):
        tradesTool = orderbook_pb2.TradesInfo()
        tradesTool.ParseFromString(byteStream)

        cursor = connection.cursor()

        try:
            for trade in tradesTool.trades:
                cursor.execute("insert into trades values(\'"+trade.exchange+"\',\'"+trade.symbol+"\',"+str(trade.timestamp)+",\'"+trade.datetime+"\',\'"+trade.side+"\',"+str(trade.price)+","+str(trade.amount)+")")
        except BaseException as e:
            print("* * * * * * * * * * Error! * * * * * * * * * *\n", e)
            return False

        return True
