from dbcreds import production_mode
import dbhelpers as dbh
from flask import Flask, request, make_response
import apihelpers as apih
import json
from flask_cors import CORS
from uuid import uuid4

app = Flask(__name__)
CORS(app)

# ## CLIENT -- get, post, patch, delete

# use the proper decoration for the necessary endpoint. .get / .post /.delete /.patch
# .get will use args. this endpoint verifies an id is being recieved. calls the procedure that takes the id and will display the client details related to that id
@app.get('/api/client')
def get_client():
# is_valid is using a helper function that will check for the data, and loop through the expected data and compare it with the sent data. if there is 
# missing link, it will prompt an error with the specific missing data that needs to be included.
    is_valid = apih.check_endpoint_info(request.args, ['id'])
    if(is_valid != None):
        return make_response(json.dumps(is_valid, default=str), 400)

# there is only one argument expected, seen by the 1 ?
    results = dbh.run_statement('CALL client_get(?)', [request.args.get('id')])

# if the type of result is a list, meaning something has worked and been gathered, this will send an ok message that the procedure has worked
# if the expected data did not return then an error message will be prompted. As this function has already determined the user error/success outcome, at this
# point of failure is on the server side. Though, better error handling could be more specific in understanding what has gone wrong.
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


# when using a header for data request.headers/.get() is used instead of request.json. In postman this information is put in the header section instead of body
@app.delete('/api/client')
def delete_client():
    is_valid = apih.check_endpoint_info(request.json, ['password'])
    if(is_valid != None):
        return make_response(json.dumps(is_valid, default=str), 400)
    
    # attempting to get token into this mix for client_delete. erroring "client_delete does not exist."
    token = dbh.run_statement('CALL client_token(?)', request.headers.get('id'))
   
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

    

# ## CLIENT LOGIN - post, delete

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

#  ## RESTARUANTS - get
@app.get('/api/restaurants')
def get_all_restaurants():
    results = dbh.run_statement('CALL restaurants_get_all')
    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps("sorry, error", default=str), 500)    

# ## RESTAURANT -get, post, (patch, delete)
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


# ## RESTAURANT LOGIN - post, delete
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

# ###MENU - get, post, delete, (patch)

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


# CLIENT_ORDER
# @app.get('/api/client_order')
# def get_client_order():

# @app.post('api/client_order')
# def create_client_order():





if (production_mode == True):
    print("Running in Production Mode")
    importbjoern# type: ignore
    bjoern.run(app, "0.0.0.0", 5042)
else:
    from flask_cors import CORS
    CORS(app)
    print("Running in Testing Mode!")
    app.run(debug=True)
