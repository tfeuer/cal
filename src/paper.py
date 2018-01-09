from bittrex.bittrex import *
import pickle
import os
from core import *

# A PaperTrader is full of Portfolios, which are full of Trades/Positions
class PaperTrader:
    def __init__(self):
        self.selected_portfolio = None
        self.portfolios = {}

        if not os.path.exists("portfolios.p"):
            self.persist_to_file()

        self.load_from_file()

    def create_new_portfolio(self, name):
        new_portfolio = Portfolio(name)
        self.portfolios[name] = new_portfolio
        self.selected_portfolio = self.portfolios[name]

    def remove_portfolio(self, name):
        del self.portfolio[name]

    def list_portfolios(self):
        for portfolio in self.portfolios:
            print portfolio

    def select_portfolio(self, name):
        try:
            self.selected_portfolio = self.portfolios[name]
            print "Selected portfolio: " + name
        except KeyError:
            print "Portfolio name not found"

    def get_name(self):
        if self.selected_portfolio == None:
            return "No portfolio selected"
        else:
            return self.selected_portfolio.name

    def persist_to_file(self):
        pickle.dump(self.portfolios, open("portfolios.p", "wb"))

    def load_from_file(self):
        self.portfolios = pickle.load(open("portfolios.p", "rb"))

class Portfolio:
    def __init__(self, name):
        self.name = name
        self.open_trades = {}

        if not os.path.exists("tradedata.p"):
            self.persist_trades()

        self.load_trades()

    # TODO: - Argument to add whether the price is bid/ask
    def open_new_trade(self, currency):
        try:
            price = BittrexConnection.connection.get_ticker("BTC-" + currency)["result"]["Ask"]
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
        for key in self.open_trades:
            self.open_trades[key].print_trade_status()

    def score_all_trades(self):
        total_score = 0.0

        for key in self.open_trades:
            total_score += self.open_trades[key].get_percent_change()

        total_score -= len(self.open_trades)
        return total_score * 100.0

    def close_all_trades(self, output_file="portfolio.txt"):
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

class Trade:
    def __init__(self, currency, buy_in):
        self.currency = currency
        self.buy_in = buy_in
        self.current_price = buy_in

    def get_current_price(self):
        current_price = BittrexConnection.connection.get_ticker("BTC-" + self.currency)["result"]["Ask"]
        return current_price

    def get_percent_change(self, ping_api=False):
        if ping_api:
            self.current_price = self.get_current_price()

        percent_change = (self.current_price / self.buy_in)
        return percent_change

    def print_trade_status(self):
        try:
            self.current_price = self.get_current_price()

            print ('%5s' % self.currency) + " |",
            print str("%1.8f" % self.current_price) + " / " + str("%1.8f" % self.buy_in) + " |",

            percent_change = (self.current_price / self.buy_in)

            print ('{%2f}' % percent_change)

        except TypeError:
            print self.currency + " .. API timeout"

    def close(self):
        self.current_price = self.get_current_price()
        percent_change = (self.current_price / self.buy_in)
        print "Closing " + self.currency + " position with score: " + ('{%2f}' % percent_change)
