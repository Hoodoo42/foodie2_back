import json
import dbhelpers as dbh

def make_api(statement):
    results = dbh.run_statement(statement)
    if (type(results) == list):
        animal_json = json.dumps(results, default=str)
        return animal_json
    else:
        return "Sorry there is an error"

def check_endpoint_info(sent_data, expected_data):
    for data in expected_data:
        if(sent_data.get(data) == None):
            return f"The {data} argument is required!"