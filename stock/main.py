import requests
import cgi

urlbase = 'http://query.yahooapis.com/v1/public/yql?q={0}&env=store://datatables.org/alltableswithkeys&format=json'
querybase = 'select * from yahoo.finance.quotes where symbol in ("{0}")'

def yql(query):
    response = requests.get(urlbase.format(query))
    return response.json()

def get_json(symbol):
    query = querybase.format(symbol)
    json = yql(query)
    return json['query']['results']['quote']

def get_price(symbol):
    return str(get_json(symbol)['LastTradePriceOnly'])

def get_name(symbol):
    return str(get_json(symbol)['Name'])

def get_open(symbol):
    return str(get_json(symbol)['Open'])

def get_high(symbol):
    return str(get_json(symbol)['YearHigh'])

def get_low(symbol):
    return str(get_json(symbol)['YearLow'])

def get_vol(symbol):
    return str("%.2f" % (float(get_json(symbol)['Volume']) / 1000000))
