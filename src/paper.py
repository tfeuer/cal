from bittrex.bittrex import *
import pickle
import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class PaperTrader:
    bittrex_connection = Bittrex(None, None)

    def __init__(self):
        # print "Paper trading initializing
        self.open_trades = {}

        if not os.path.exists("tradedata.p"):
            self.persist_trades()

        self.load_trades()

    def open_new_trade(self, currency):
        price = PaperTrader.bittrex_connection.get_ticker("BTC-" + currency)["result"]["Ask"]
        new_trade = Trade(currency, price)

        if currency not in self.open_trades:
            self.open_trades[currency] = new_trade
            print 'Opened ' + currency + ' at ' + '%1.8f' % price
        else:
            print 'Position already open'

    def close_trade(self, currency):
        if currency in self.open_trades:
            self.open_trades[currency].close()
            del self.open_trades[currency]

    def list_open_trades(self):
        # print 'CURRENT POSITIONS'

        for key in self.open_trades:
            self.open_trades[key].print_trade_status()

    def persist_trades(self):
        pickle.dump(self.open_trades, open("tradedata.p", "wb"))

    def load_trades(self):
        self.open_trades = pickle.load(open("tradedata.p", "rb"))

    def lookup_price(self, currency):
        current_price = PaperTrader.bittrex_connection.get_ticker("BTC-" + currency)["result"]["Ask"]
        print '%1.8f' % current_price

class Trade:
    def __init__(self, currency, buy_in):
        self.currency = currency
        self.buy_in = buy_in

    def get_current_price(self):
        current_price = PaperTrader.bittrex_connection.get_ticker("BTC-" + self.currency)["result"]["Ask"]
        return current_price

    def print_trade_status(self):
        self.current_price = self.get_current_price()

        print ('%5s' % self.currency) + " |",
        print str("%1.8f" % self.current_price) + " / " + str("%1.8f" % self.buy_in) + " |",

        percent_change = (self.current_price / self.buy_in)

        print bcolors.OKBLUE + ('{%2f}' % percent_change) + bcolors.ENDC

    def close(self):
        self.current_price = self.get_current_price()

        percent_change = (self.current_price / self.buy_in)
        print "Closing " + self.currency + " position with score: " + ('{%2f}' % percent_change)
