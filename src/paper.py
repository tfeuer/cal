from bittrex.bittrex import *
import pickle
import os

class PaperTrader:
    bittrex_connection = Bittrex(None, None)

    def __init__(self):
        # print "Paper trading initializing"
        self.open_trades = {}

        if not os.path.exists("tradedata.p"):
            self.persist_trades()

        self.load_trades()

    def open_new_trade(self, currency):
        try:
            price = PaperTrader.bittrex_connection.get_ticker("BTC-" + currency)["result"]["Ask"]
            new_trade = Trade(currency, price)

            if currency not in self.open_trades:
                self.open_trades[currency] = new_trade
                print 'Opened ' + currency + ' at ' + '%1.8f' % price
            else:
                print 'Position already open'
        except TypeError:
            print 'Currency not found'


    def close_trade(self, currency):
        if currency in self.open_trades:
            self.open_trades[currency].close()
            del self.open_trades[currency]

    def list_open_trades(self):
        # print 'CURRENT POSITIONS'
        for key in self.open_trades:
            self.open_trades[key].print_trade_status()

    def score_all(self):
        total_score = 0.0

        for key in self.open_trades:
            total_score += self.open_trades[key].get_percent_change()

        total_score -= len(self.open_trades)
        return total_score * 100.0

    def close_all(self, output_file="portfolio.txt"):
        f = open(output_file, 'w')

        total_score = self.score_all()

        for key in self.open_trades:
            f.write(' '.join((key, '%2.2f' % self.open_trades[key].get_percent_change())))
            f.write('\n')
            self.open_trades[key].close()

        self.open_trades = {}

        f.write(' '.join(("Total score", str(total_score))))
        f.close()

    def persist_trades(self):
        pickle.dump(self.open_trades, open("tradedata.p", "wb"))

    def load_trades(self):
        self.open_trades = pickle.load(open("tradedata.p", "rb"))

    def lookup_price(self, currency):
        try:
            current_price = PaperTrader.bittrex_connection.get_ticker("BTC-" + currency)["result"]["Ask"]
            print '%1.8f' % current_price
        except TypeError:
            print 'Not found'

class Trade:
    def __init__(self, currency, buy_in):
        self.currency = currency
        self.buy_in = buy_in
        self.current_price = buy_in

    def get_current_price(self):
        current_price = PaperTrader.bittrex_connection.get_ticker("BTC-" + self.currency)["result"]["Ask"]
        return current_price

    def print_trade_status(self):
        try:
            self.current_price = self.get_current_price()

            print ('%5s' % self.currency) + " |",
            print str("%1.8f" % self.current_price) + " / " + str("%1.8f" % self.buy_in) + " |",

            percent_change = (self.current_price / self.buy_in)

            print ('{%2f}' % percent_change)
            
        except TypeError:
            print self.currency + " .. API timeout"

    def get_percent_change(self, ping_api=False):
        if ping_api:
            self.current_price = self.get_current_price()

        percent_change = (self.current_price / self.buy_in)
        return percent_change

    def close(self):
        self.current_price = self.get_current_price()
        percent_change = (self.current_price / self.buy_in)
        print "Closing " + self.currency + " position with score: " + ('{%2f}' % percent_change)
