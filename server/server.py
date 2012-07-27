#!/usr/bin/env python
#encoding=utf-8
from flask import Flask,  request, render_template
from data import dogfoodproduct, pool
import json

app = Flask(__name__)

# decorator: checking product is exists
def need_product(func):
    def _dec(*args, **kw):
        pn = kw['pn']
        print pn
        df = dogfoodproduct(pn)
        print df
        if df is None: return json.dumps({'ret':-1})
        return func(*args, **kw)
    return _dec

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

@need_product
@app.route('/action/<pn>/<action>')
def do_action(pn, action):
    df = dogfoodproduct(pn)
    username = request.args.get('u', '')
    if df.is_user_enable(username):
        df.record_action(username, action)
        return "OK"
    return "user not enable"

@need_product
@app.route('/list/action/<pn>/<action>')
def do_get_action_list(pn, action):
    df = dogfoodproduct(pn)
    return json.dumps(df.get_action_list(action))


@app.route('/list/<pn>')
@need_product
def do_list(pn):
    df = dogfoodproduct(pn)
    items = df.get_users()
    return json.dumps(items)

@need_product
@app.route('/list/<pn>/add', methods=['POST'])
def do_add(pn):
    df = dogfoodproduct(pn)
    if df.add_user(request.form.get('u', None)):
        return json.dumps({'ret': 1})
    return json.dumps({'ret':-1})

@need_product
@app.route('/list/<pn>/addmulti', methods=['POST'])
def do_add(pn):
    df = dogfoodproduct(pn)
    names = request.form.get('u', '')
    names = names.split('\n')
    cnt = 0
    for name in names:
        if df.add_user(name.rstrip().lstrip()):
            cnt+=1
    return json.dumps({'ret':cnt})

@need_product
@app.route('/list/<pn>/toggle')
def do_remove(pn):
    df = dogfoodproduct(pn)
    uname = request.args.get('u', '')
    df.toggle_user_enable_status(uname)
    return json.dumps({'ret':1})

@need_product
@app.route('/list/<pn>/delete')
def do_delete(pn):
    df = dogfoodproduct(pn)
    uname = request.args.get('u', '')
    if df.delete_user(uname):
        return json.dumps({'ret':1})
    return json.dumps({'ret':0})

@need_product
# 检查用户是否在白名单中
@app.route('/check/<pn>')
def do_check(pn):
    df = dogfoodproduct(pn)
    if df.is_user_enable(request.args.get('u','')):
        return json.dumps({'ret': 1})
    return json.dumps({'ret':-1})


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
