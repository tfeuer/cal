from bittrex.bittrex import *

class BittrexConnection(object):
    connection = Bittrex(None, None)

    @staticmethod
    def lookup_ask_price(currency):
        price = BittrexConnection.connection.get_ticker("BTC-" + currency)["result"]["Ask"]
        return price

    @staticmethod
    def lookup_bid_price(currency):
        price = BittrexConnection.connection.get_ticker("BTC-" + currency)["result"]["Bid"]
        return price

    @staticmethod
    def display_price(currency):
        prices = BittrexConnection.connection.get_ticker("BTC-" + currency)["result"]
        print 'Bid: ' + '%1.8f' % prices["Bid"]
        print 'Ask: ' + '%1.8f' % prices["Ask"]

    @staticmethod
    def test_func(currency):
        data = BittrexConnection.connection.get_ticker("BTC-" + currency)
        print data
