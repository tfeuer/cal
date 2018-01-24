# cal
Crypto paper trading and bittrex CLI client

You can use this CLI tool to (currently just) paper trade on Bittrex.

Commands are as follows:

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

### status \<symbol\>

Shows percentage gain/loss of a given position 
