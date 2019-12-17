# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 22:17:56 2019

@author: David
"""
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import requests
import json
import time
from multiprocessing import Process, Value
#%% Import Credentials 
with open('credentials.json') as json_data:
    credentials = json.load(json_data)

# %% Start the Service
account_sid = credentials['account_sid']
auth_token = credentials['auth_token']
client = Client(account_sid,auth_token)
phone_number = credentials['phone_number']
# %% Set up the Responses
app = Flask(__name__)

def shutdown_server():
    p.terminate()
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the werkzeug server')
    func()

def get_cat_fact():
    PARAMS = {"max_length":256}
    cat_response = requests.get("https://catfact.ninja/fact", params = PARAMS)
    cat_json = cat_response.json()
    cat_fact = cat_json["fact"]
    return cat_fact 

def cat_feed():
    starttime=time.time()
    while True:
        message = client.messages.create(
            body = get_cat_fact(),
            from_ = '+19785255016',
            to = phone_number)
        time.sleep(60.0 - ((time.time() - starttime) % 60.0))

@app.route("/sms", methods=['GET', 'POST'])
#this is all stuff that happens once the server receives an incoming request
def sms_ahoy_reply():
    #Look at content of message
    body = request.values.get('Body', None)
    
    resp = MessagingResponse()
    if body == 'HALT':
        res = requests.post('http://localhost:5000/shutdown')
        return res
    else:  
        resp.message(get_cat_fact())
        return str(resp)

@app.route("/shutdown", methods =['POST'])
def shutdown():
    message = client.messages.create(
            body = 'You will now be unsubscribed to Cat Facts.',
            from_ = '+19785255016',
            to = phone_number)
    shutdown_server()
    
   

if __name__ == "__main__":
    text = "Thank you for subscribing to Cat Facts!\nYou will receive a new cat fact every 5 minutes."
    text1 = "Reply MORE to get more Cat facts. Reply HALT to unsubscribe"
    
    message = client.messages.create(
        body = text,
        from_ = '+19785255016',
        to = phone_number )

    message1 = client.messages.create(
        body = text1,
        from_ = '+19785255016',
        to = phone_number)
    #set up multiprocessing
    process_params = Value('b', True)
    p = Process(target=cat_feed,args=())
    p.start()
    app.run(debug=True, use_reloader=False)
    p.join()