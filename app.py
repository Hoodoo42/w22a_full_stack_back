
import dbhelpers as dbh
from flask import Flask, request, make_response
import apihelpers as apih
import json

app = Flask(__name__)

@app.get('/api/candy')
def get_candy():
    # no input to validate so straight to run statement
    results = dbh.run_statement('CALL get_candy()')
# if result of run_statement is a list tpye then return a success message else send a server error message
    if(type(results) == list):
      return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps('Error'), 500)

@app.post('/api/candy')
def add_candy():
    is_valid = apih.check_endpoint_info(request.json, ['name', 'img_url', 'description'])
    if(is_valid != None):
        return make_response(json.dumps(is_valid, default=str), 400)

    results = dbh.run_statement('CALL add_candy(?,?,?)', [request.json.get('name'), request.json.get('img_url'), request.json.get('description')])

    if(type(results) == list):
        return make_response(json.dumps(results[0][0], default=str), 200)
    else: 
        return make_response(json.dumps('Error', default=str), 500)

@app.delete('/api/candy')
def delete_candy():
    is_valid = apih.check_endpoint_info(request.json, ['id'])
    if(is_valid != None):
        return make_response(json.dumps(is_valid, default=str), 400)

    results = dbh.run_statement('CALL delete_candy(?)', [request.json.get('id')])

    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else: 
        return make_response(json.dumps('Error', default=str), 500)

app.run(debug=True) 