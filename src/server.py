#!/usr/bin/env python
#  coding: utf-8

from flask import Flask, jsonify, request, abort, url_for, render_template, flash, redirect
from flask import json
import os.path
import urllib.parse
import urllib.request

#- init db
import db
if not os.path.exists('fet.db'):
    print ('database init')
    db.create_tables()

app = Flask(__name__)
app.secret_key ="SDFfeSfsF23f3sfS5T%78ugs"

#- int to base36 alpahnumeric    
def base36(num,base=36, numerals="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    return ((num == 0) and numerals[0]) or (base36(num // base, base, numerals).lstrip(numerals[0]) + numerals[num % 36])    

#- converts table index to ebury test specific format TRXXXXXXX
def gen_id():
    mask = "TR0000000"
    try: index = db.Trades.select().order_by(db.Trades.index.desc()).get().index
    except: index = 0
    alpha_index = base36(index)
    id = mask[:-len(alpha_index)]+alpha_index
    print ("id = ", id)
    return id

#- get trading rate from fixer.io
def get_rate(sell_currency, buy_currency):
    params = urllib.parse.urlencode({'base': sell_currency, 'symbols':buy_currency})
    url = "http://api.fixer.io/latest?%s" % params
    with urllib.request.urlopen(url) as f:rate=f.read().decode('utf-8')
    return json.loads(rate)['rates'][buy_currency]


@app.route('/')
@app.route('/index.html')
def index():
    str(request.remote_addr)
    trades=[]
    for item in db.Trades.select().limit(50):
        trade=[]
        trade.append(item.sell_currency)
        trade.append(item.sell_amount)
        trade.append(item.buy_currency)
        trade.append(item.buy_amount)
        trade.append(item.rate)
        trade.append(item.date_booked)
        trades.append(trade)
        
    return render_template('index.html', result=trades)
    

"""
Some magic here, you can post using the webform but you can also create a new entry 
using it like a JSON restaip, example:
curl -H "Content-Type: application/json" -X POST -d '{"sell_currency":"EUR", "sell_amount":222 ,"buy_currency":"AUD"}' http://127.0.0.1:8000/trade.html
""" 

@app.route('/trade.html', methods = ['POST','GET'])
def trade():
    
    if request.method == 'GET': return render_template('trade.html')
    
    if  request.json:
        if request.get_json() == None or set((list(request.get_json().keys()))) != set(['sell_currency','sell_amount','buy_currency']): 
            return abort(400)
        sell_currency = request.json['sell_currency']
        sell_amount   = request.json['sell_amount']
        buy_currency  = request.json['buy_currency']
    else:
        sell_currency = request.form['sell_currency']
        sell_amount   = float(request.form['sell_amount'])
        buy_currency  = request.form['buy_currency']
    
    if sell_currency == buy_currency: return abort(400)
    
    rate = get_rate(sell_currency,buy_currency)

    trade  = db.Trades(id            = gen_id(),
                       sell_currency = sell_currency,
                       sell_amount   = sell_amount,
                       buy_currency  = buy_currency,
                       buy_amount    = sell_amount*rate,
                       rate          = rate)
                       
    result = trade.save()

    if request.json: return jsonify(True)
    else:
        flash('Trade done') 
        return render_template('trade.html')
    
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(8000), debug=False)

