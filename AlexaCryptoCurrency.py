import logging
import Coinbase


from random import randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session

'''
RFQIntent Can you please give the price for {currency}
ConseilIntent Do you think it's the good time to {way} {currency}
OrderIntent {way} {quantity} {currency}
PriceForGivenSizeIntent what is the price if I want to {way} {quantity} {currency}
EndSessionIntent Thank you
EndSessionIntent Bye
EndSessionIntent Good bye
EndSessionIntent Thanks
'''


app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch

def new_session():

    welcome_msg = render_template('welcome')

    return question(welcome_msg)


@ask.intent("RFQIntent", convert={'currency': str})

def REQ(currency):

    if (currency == "bitcoin"):
        p = Coinbase.GetPrice('BTC')
        return question(render_template("RFQ",  ccy=currency, price=p))
    if (currency == "ethereum"):
        p = Coinbase.GetPrice('ETH')
        return question(render_template("RFQ",  ccy=currency, price=p))
    else:
        return statement(render_template('Cannothelp'))


@ask.intent("ConseilIntent", convert={'way': str, 'currency': str})

def Conseil(way, currency):
    if Coinbase.isLeadLag(way == "buy", 'BTC', 'ETH'):
        return question(render_template('ConseilLeadLagGoodtime', way=way, currency=currency))
    else:
        return question(render_template('ConseilLeadLagBadtime', way=way, currency=currency))



@ask.intent("PriceForGivenSizeIntent", convert={'way': str, 'quantity':int,'currency': str})
def PriceForGiveSize(way, quantity, currency):
    if (currency == "bitcoin"):
        price = Coinbase.GetPriceForQuantity(way == 'buy', 'BTC', quantity)
        msg = render_template('PriceForGivenSize', way=way, qty=quantity, currency=currency, price=price)
        return question(msg)
    elif (currency == "ethereum"):
        price = Coinbase.GetPriceForQuantity(way == 'buy', 'ETH', quantity)
        msg = render_template('PriceForGivenSize', way=way, qty=quantity, currency=currency, price=price)
        return question(msg)


@ask.intent("OrderIntent", convert={'way': str, 'quantity':int,'currency': str})

def ReceiveOrder(way, quantity, currency):

    msg = render_template('Done', way=way, qty=quantity,currency =currency)

    return question(msg)

@ask.intent("EndSessionIntent")

def EndSession():
    return statement("Sure, bye!")


if __name__ == '__main__':

    app.run(debug=True)