#!/usr/bin/env python
from flask import Flask,  request, render_template
from data import dogfoodproduct, pool
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<pn>')
def product_page(pn):
    return render_template('list.html', usrs = [], product = pn)


###################### AJAX ######################
@app.route('/productlist')
def do_productlist():
    return json.dumps(pool.get_product_list())

@app.route('/addproduct', methods=['POST'])
def do_addproduct():
    pn = request.form['pn']
    pool.add_product(pn)
    return 'OK'

@app.route('/action/<pn>/<username>/<action>')
def do_action(pn, username, action):
    df = dogfoodproduct(pn)
    if df is None: return json.dumps({'ret':-1})
    df.record_action(username, action)
    return "OK"

@app.route('/list/<pn>')
def do_list(pn):
    df = dogfoodproduct(pn)
    if df is None: return json.dumps({'ret':-1})
    items = df.get_users()
    return json.dumps(items)

@app.route('/list/<pn>/add', methods=['POST'])
def do_add(pn):
    df = dogfoodproduct(pn)
    if df is None: return json.dumps({'ret':-1})
    if df.add_user(request.form.get('u', None)):
        return json.dumps({'ret': 0})
    return json.dumps({'ret':-1})

@app.route('/list/<pn>/toggle')
def do_remove(pn):
    df = dogfoodproduct(pn)
    if df is None: return json.dumps({'ret':-1})
    uname = request.args.get('u', '')
    df.toggle_user_enable_status(uname)

@app.route('/check/<pn>')
def do_check(pn):
    df = dogfoodproduct(pn)
    if df is None: return json.dumps({'ret':-1})
    if df.is_user_enable(request.args.get('u','')):
        return json.dumps({'ret': 0})
    return json.dumps({'ret':-1})


if __name__ == '__main__':
    app.run()
