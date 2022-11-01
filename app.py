from lib2to3.pgen2 import token
from signal import default_int_handler
from unittest import result
from dbcreds import production_mode
import dbhelpers as dbh
from flask import Flask, request, make_response
import apihelpers as apih
import json
from flask_cors import CORS
from uuid import uuid4

app = Flask(__name__)
CORS(app)

# ## CLIENT

@app.get('/api/client')
def get_client():
    is_valid = apih.check_endpoint_info(request.args, ['id'])
    if(is_valid != None):
        return make_response(json.dumps(is_valid, default=str), 400)

    results = dbh.run_statement('CALL client_get(?)', [request.args.get('id')])

    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps('Sorry Error', default=str), 500)

@app.post('/api/client')
def create_client():
    is_valid = apih.check_endpoint_info(request.json, ['email', 'first_name', 'last_name', 'username', 'img_url', 'password'])
    if(is_valid != None):
        return make_response(json.dumps(is_valid, default=str), 400)

    results = dbh.run_statement('CALL client_create(?,?,?,?,?,?)', [request.json.get('email'), request.json.get('first_name'), request.json.get('last_name'), request.json.get('username'), request.json.get('img_url'), request.json.get('password')])
    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps("sorry error", default=str), 500)        

@app.delete('/api/client')
def delete_client():
    is_valid = apih.check_endpoint_info(request.json, ['password'])
    if(is_valid != None):
        return make_response(json.dumps(is_valid, default=str), 400)
    token = dbh.run_statement('CALL client_token(?)', request.headers.get('token'))
    results = dbh.run_statement('CALL client_delete(?,?)', [token, request.json.get('password')])
    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps("sorry error", default=str), 500)    

@app.patch('/api/client')
def update_client():
    

    results = dbh.run_statement('CALL client_update(?,?,?,?,?,?,?)', [request.headers.get('token'), request.json.get('email'), request.json.get('first_name'), request.json.get('last_name'), request.json.get('username'), request.json.get('img_url'), request.json.get('password')])
    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else: 
        return make_response(json.dumps('sorry error', default=str), 500)       

    

# ## CLIENT LOGIN

@app.post('/api/client_login')
def login_client():
    is_valid = apih.check_endpoint_info(request.json, ['email', 'password'])
    if(is_valid != None):
        return make_response(json.dumps(is_valid, default=str), 400)

    token = uuid4().hex
    results = dbh.run_statement('CALL client_login(?,?,?)', [request.json.get('email'), request.json.get('password'), token])   
    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps('sorry, error', default=str), 500)
        

# delete token for client logout. token is from client_session.
@app.delete('/api/client_login')
def logout_client():
    is_valid = apih.check_endpoint_info(request.headers, ['token'])
    if(is_valid != None):
        return make_response(json.dumps(is_valid, default=str), 400)

    results = dbh.run_statement('CALL client_logout(?)', [request.headers.get('token')])
    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else: 
        return make_response(json.dumps('sorry error', default=str), 500)       

#  ## RESTARUANTS
@app.get('/api/restaurants')
def get_all_restaurants():
    results = dbh.run_statement('CALL restaurants_get_all')
    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps("sorry, error", default=str), 500)    
# ## RESTAURANT
@app.get('/api/restaurant')
def get_restaurant():
    is_valid = apih.check_endpoint_info(request.args, ['id'])
    if(is_valid != None):
        return make_response(json.dumps(is_valid, default=str), 400)


    results = dbh.run_statement('CALL restaurant_get(?)', [request.args.get('id')])
    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps("sorry error", default=str), 500)

@app.post('/api/restaurant')
def create_restaurant():
    is_valid = apih.check_endpoint_info(request.json, ['email', 'name', 'address', 'city', 'phone_num', 'bio', 'password'])
    if(is_valid != None):
        return make_response(json.dumps(is_valid, default=str), 400)

    results = dbh.run_statement('CALL restaurant_create(?,?,?,?,?,?,?)', [request.json.get('email'), request.json.get('name'), request.json.get('address'), request.json.get('city'), request.json.get('phone_num'),request.json.get('bio'), request.json.get('password')])
    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps("sorry error", default=str), 500) 


# ## RESTAURANT LOGIN
@app.post('/api/restaurant_login')
def login_restaurant():
    is_valid = apih.check_endpoint_info(request.json, ['email', 'password'])
    if(is_valid != None):
        return make_response(json.dumps(is_valid, default=str), 400)

    token = uuid4().hex
    results = dbh.run_statement('CALL restaurant_login(?,?,?)', [request.json.get('email'), request.json.get('password'), token])   
    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps('sorry, error', default=str), 500)

@app.delete('/api/restaurant_login')
def logout_restaurant():
    is_valid = apih.check_endpoint_info(request.headers, ['token'])
    if(is_valid != None):
        return make_response(json.dumps(is_valid, default=str), 400)

    token = uuid4().hex
    results = dbh.run_statement('CALL restaurant_logout(?)', [request.headers.get('token')])   
    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps('sorry, error', default=str), 500)

# ###MENU

# create_menu procedure works in db, does not hit any errors in postman/vs however also does not insert new item into menu_item table
@app.post('/api/menu')
def create_menu():
    is_valid = apih.check_endpoint_info(request.json, ['name', 'description', 'img', 'price'])
    if(is_valid != None):
        return make_response(json.dumps(is_valid, default=str), 400)


    results = dbh.run_statement('CALL menu_item_create(?,?,?,?,?)', [request.json.get('name'), request.json.get('description'), request.json.get('img'), request.json.get('price'), request.headers.get('token')])
    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps("sorry error", default=str), 500)


# returns all menu items associated with a restaurant
@app.get('/api/menu')
def get_menu():
    is_valid = apih.check_endpoint_info(request.args, ['restaurant_id'])
    if(is_valid != None):
        return make_response(json.dumps(is_valid, default=str), 400)

    results = dbh.run_statement('CALL menu_get(?)', [request.args.get('restaurant_id')])                
    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps('sorry error', default=str), 500)    

@app.delete('/api/menu')
def delete_menu_itme():
    is_valid = apih.check_endpoint_info(request.json, ['menu_id'])
    if(is_valid != None):
        return make_response(json.dumps(is_valid, default=str), 400)

    results = dbh.run_statement('CALL menu_item_delete(?,?)', [request.headers.get('token'), request.json.get('menu_id')])
    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps('sorry error', default=str), 500)    

if (production_mode == True):
    print("Running in Production Mode")
    importbjoern# type: ignore
    bjoern.run(app, "0.0.0.0", 5042)
else:
    from flask_cors import CORS
    CORS(app)
    print("Running in Testing Mode!")
    app.run(debug=True)
