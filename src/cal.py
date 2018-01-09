from bittrex.bittrex import *
from paper import *
from core import *

paper_trader = PaperTrader()

CLI_COMMANDIN_STRING = "cal {  "
argv = raw_input(CLI_COMMANDIN_STRING).split()
argc = len(argv)

base_command = ""

if argc != 0:
    base_command = argv[0]

while base_command != "quit" and base_command != "q":
    # general commands
    if base_command == "test":
        BittrexConnection.test_func("nxt")

    if base_command == "price" and argc == 2:
        # print 'Bid: ' + '%1.8f' % BittrexConnection.lookup_bid_price(argv[1].upper())
        # print 'Ask: ' + '%1.8f' % BittrexConnection.lookup_ask_price(argv[1].upper())
        BittrexConnection.display_price(argv[1])

    # portfolio commands

    if base_command == "portfolios":
        paper_trader.list_portfolios()

    if base_command == "newportfolio" and argc == 2:
        paper_trader.create_new_portfolio(argv[1])

    if base_command == "portfolio":
        if argc == 1:
            print paper_trader.get_name()
        if argc == 2:
            paper_trader.select_portfolio(argv[1])

    # trade commands

    if base_command == "open" and argc == 2:
        paper_trader.selected_portfolio.open_new_trade(argv[1].upper())

    if base_command == "close" and argc == 2:
        paper_trader.selected_portfolio.close_trade(argv[1].upper())

    if base_command == "status" and argc == 1:
        paper_trader.selected_portfolio.list_open_trades()

    if base_command == "status" and argc == 2:
        if argv[1].upper() in paper_trader.selected_portfolio.open_trades:
            paper_trader.selected_portfolio.open_trades[argv[1].upper()].print_trade_status()
        else:
            print "No position"

    if base_command == "scoreall":
        print paper_trader.selected_portfolio.score_all_trades()

    if base_command == "closeall":
        if argc == 2:
            filename = argv[1]
            paper_trader.selected_portfolio.close_all_trades(filename)
        else:
            print "Please provide a filename"

    # Next command
    argv = raw_input(CLI_COMMANDIN_STRING).split()
    argc = len(argv)
    if argc != 0:
        base_command = argv[0]
    else:
        base_command = ""

paper_trader.persist_to_file()
