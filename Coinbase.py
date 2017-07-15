from coinbase.wallet.client import Client
import urllib2

import json
key = "5phviZA2qe5X0tqq"
secret = "lvdVQrj9QsmkkwTT7y14Hqd8vhKUCsR4"
client = Client(key, secret)


def GetPrice(ccy):
    rates = client.get_exchange_rates(currency=ccy)
    return rates["rates"]["USD"]

from coinbase.wallet.model import APIObject

def Get5DaysPrice(ccy):
    #price = client.get_spot_price(currency_pair=ccy +'-USD', date="2017-06-13")
    res = []
    #price = client.get_historic_prices(currency_pair=ccy +'-USD')
    price = client._make_api_object(client._get('v2', 'prices', ccy + '-USD', 'historic'), APIObject)

    for i in range(5):
        res.append(float(price['prices'][i]['price']))
    return res

def GetWeightPrice(ccy):
    prices = Get5DaysPrice(ccy)
    return (0.5 * prices[0] + 0.4 * prices[1] + 0.3 * prices[2] + 0.2 * prices[3] + 0.1 * prices[4]) / 1.5

def GetReturn(ccy):
    prices = Get5DaysPrice(ccy)
    return (prices[0] - prices[4]) / prices[4]


def isTrendFollowing(isbuy, ccy):
    wp = GetWeightPrice(ccy)
    spot = GetPrice(ccy)
    if (spot > wp):
        return isbuy
    else:
        return not isbuy

def isLeadLag(isbuy, ccy1, ccy2):
    return1 = GetReturn(ccy1)
    return2 = GetReturn(ccy2)

    if (return1 * return2 > 0 and abs(return1) < abs(return2)):
        if (return1>0):
            return isbuy
        else:
            return not isbuy
    return False

def GetPriceForQuantity(isBuy, ccy, qty):
    response = urllib2.urlopen("https://api.cryptowat.ch/markets/gdax/" + ccy +"usd/orderbook")
    data = response.read()
    if (isBuy):
        prices = json.loads(data)["result"]["asks"]
    else:
        prices = json.loads(data)["result"]["bids"]
    initqty = qty
    nominal = 0
    for level in prices:
        qty = qty - level[1]
        if (qty <=0):
            nominal = nominal + level[0] * (level[1] + qty)
            break
        nominal = level[0] * level[1] + nominal
    return nominal / initqty

if __name__ == '__main__':
    print GetPriceForQuantity(False, 'btc', 3)
    print GetReturn('BTC')
    print GetReturn('ETH')
    print isLeadLag(True, "BTC", "ETH")
    #print client.get_currencies()