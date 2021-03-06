from bittrex.bittrex import *
from paper import *
from gold import *
from core import *

paper_trader = PaperTrader()
gold_trader = GoldTrader()

CLI_COMMANDIN_STRING = "cal {  "
argv = raw_input(CLI_COMMANDIN_STRING).split()
argc = len(argv)

base_command = ""

if argc != 0:
    base_command = argv[0]

while base_command != "quit" and base_command != "q":
    # General commands
    if base_command == "test":
        if argc == 1:
            gold_trader.get_balances()
        elif argc == 2:
            arg1 = argv[1]
            print gold_trader.get_balance_of(arg1)

    if base_command == "price" and argc == 2:
        BittrexConnection.display_price(argv[1])

    # Portfolio commands

    if base_command == "portfolios":
        paper_trader.list_portfolios()

    if base_command == "newportfolio" and argc == 2:
        paper_trader.create_new_portfolio(argv[1])

    if base_command == "portfolio":
        if argc == 1:
            print paper_trader.get_name()
        if argc == 2:
            paper_trader.select_portfolio(argv[1])

    # Trade commands

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
        paper_trader.selected_portfolio.close_all_trades()

    # Next command in
    argv = raw_input(CLI_COMMANDIN_STRING).split()
    argc = len(argv)
    if argc != 0:
        base_command = argv[0]
    else:
        base_command = ""

paper_trader.persist_to_file()
