import yahoo_finance

def price(symbol):
    fetchedprice = yahoo_finance.Share(symbol).get_price()
    if fetchedprice:
        return "One stock of " + symbol + " is $" + fetchedprice + "."
    else:
        return "That isn't a valid stock symbol."
