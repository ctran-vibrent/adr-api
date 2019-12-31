from flask import request
from app import app
from app.utils import *
import json

def errorMsg(msg):
    return json.dumps({
        'Success': False,
        'Message': msg
    })

@app.route('/checkconn')
def checkconn():
    query='SELECT * from communication_category'
    return json.dumps(mySQL_connect(query))

@app.before_request
def check_over_180():
    if 'past_days' in request.get_json():
        past_days = int(request.get_json()['past_days'])
        if past_days > 180:
            return errorMsg('Exceed 180 days range.')

@app.route('/api/click_agents', methods=['POST'])
def click_agents():
    past_days = int(request.get_json()['past_days'])
    return json.dumps(get_click_user_agents(past_days))

@app.route('/api/open_agents', methods=['POST'])
def open_agents():
    past_days = int(request.get_json()['past_days'])
    return json.dumps(get_open_user_agents(past_days))

@app.route('/api/pop_links', methods=['POST'])
def pop_links():
    past_days = int(request.get_json()['past_days'])
    return json.dumps(get_click_links(past_days))
