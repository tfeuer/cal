# cal
Crypto paper trading and bittrex CLI client

You can use this CLI tool to (currently just) paper trade on Bittrex.

Commands are as follows:

## General Commands
### price \<symbol\>

Displays the Bid and Ask price of the given symbol

### quit, q

Quits cal and persists all portfolios / positions to disk

## Portfolio Commands
### newportfolio \<name\>

Creates a new portfolio with the name you provide and automatically switches to it

### portfolios

Lists all portfolio names your client is tracking

### portfolio \<name\>

Switches to the portfolio with the name you provided

## Trade Commands
### open \<symbol\>

Adds a position to your portfolio of the provided currency at its given ask price. 

### close \<symbol\>

Closes a position with the given symbol

### status \<symbol\>

Shows percentage gain/loss of a given position 

### status

Displays all percentage gain/loss of all positions in selected portfolio

### scoreall

Calculate exact percentage point gain/loss of the selected portfolio

### closeall

Closes all positions in the selected portfolio and writes their gain/loss to a file portfolio_name.txt
