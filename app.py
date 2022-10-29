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
    is_valid = apih.check_endpoint_info(request.json, ('token', 'password'))
    if(is_valid != None):
        return make_response(json.dumps(is_valid, default=str), 400)

    results = dbh.run_statement('CALL client_delete(?,?)', [request.json.get('token'), request.json.get('password')])

# @app.patch('/api/client')
# def update_client():

# ## CLIENT LOGIN

# @app.post('/api/client_login')
# def login_client():
#     is_valid = apih.check_endpoint_info(request.json('email', 'password'))
#     if(is_valid != None):
#         return make_response(json.dumps(is_valid, default=str), 400)

#     results = dbh.run_statement('CALL client_login(?,?)', [request.json.get('email'), request.json.get('password')])   
#     if(type(results) == list):


# delete token for client logout. token is from client_session. Needs client password
# @app.delete('/api/client_login')
# def logout_client():

# needs debugging
# returns all menu items associated with a restaurant
@app.get('/api/menu')
def get_menu():
    is_valid = apih.check_endpoint_info(request.args('restaurant_id'))
    if(is_valid != None):
        return make_response(json.dumps(is_valid, default=str), 400)

    results = dbh.run_statement('CALL menu_get(?)', [request.args.get('restaurant_id')])                
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
