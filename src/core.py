from bittrex.bittrex import *
from paper import *

paper_trader = PaperTrader()

CLI_COMMANDIN_STRING = "cal {  "
argv = raw_input(CLI_COMMANDIN_STRING).split()
argc = len(argv)

base_command = ""

if argc != 0:
    base_command = argv[0]

while base_command != "quit" and base_command != "q":
    if base_command == "open" and argc == 2:
        paper_trader.open_new_trade(argv[1].upper())

    if base_command == "close" and argc == 2:
        paper_trader.close_trade(argv[1].upper())

    if base_command == "status" and argc == 1:
        paper_trader.list_open_trades()

    if base_command == "status" and argc == 2:
        if argv[1].upper() in paper_trader.open_trades:
            paper_trader.open_trades[argv[1].upper()].print_trade_status()
        else:
            print "No position"

    if base_command == "price" and argc == 2:
        paper_trader.lookup_price(argv[1].upper())

    if base_command == "scoreall":
        print paper_trader.score_all()

    if base_command == "closeall":
        if argc == 2:
            filename = argv[1]
            paper_trader.close_all(filename)
        else:
            print "Please provide a filename"

    # Next command
    argv = raw_input(CLI_COMMANDIN_STRING).split()
    argc = len(argv)
    if argc != 0:
        base_command = argv[0]
    else:
        base_command = ""

paper_trader.persist_trades()
