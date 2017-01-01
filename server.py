# -*- coding: utf-8 -*-
 # Download the library from twilio.com/docs/libraries
from twilio.rest import TwilioRestClient
import twilio.twiml
from flask import Flask
import time
import os

app = Flask(__name__)
localtime = time.asctime(time.localtime(time.time()))

@app.route("/")
def hello():
    f = open('mylog.txt', 'a')
    f.write('\nA param GET request at ' + localtime)
    f.close()
    return "Hello World!"

@app.route("/clearlog")
def clearlog():
    f = open('mylog.txt', 'w')
    f.write('')
    f.close()
    return "Cleared log file!"
    
@app.route("/read")
def read():
  f = open('mylog.txt', 'r')
  msg = f.read()
  return msg

# Get these credentials from http://twilio.com/user/account
account_sid = os.environ['env_account_sid']
auth_token = os.environ['env_auth_token']
client = TwilioRestClient(account_sid, auth_token)

# Make the call
@app.route("/call")
def call():
  call = client.calls.create(to=os.environ[TO_NUMBER],  # Any phone number
                            from_=os.environ[TWILIO_NUMBER], # Must be a valid Twilio number
                            url="https://faded-fairy.gomix.me/say")
  f = open('mylog.txt', 'a')
  f.write('\nMade the call at ' + localtime)
  f.close()
  return "Call sent!"
  
# Receive the webhook
@app.route("/say", methods=['GET', 'POST'])
def say():
  resp = twilio.twiml.Response()
  msg = u"Bom dia. Eu sou a Jásperina, uma assistente virtual programada pelo Pedro Batista. Gostaria de lhe desejar um excelente ano novo, e que 2017 nos traga grandes desafios e muitos sucessos. Adeus!"
  resp.say(msg, language="pt-PT", voice="alice")
  return str(resp)
  
# Receive the call
@app.route("/answer", methods=['GET', 'POST'])
def answer():
  resp = twilio.twiml.Response()
  msg = u"Bom dia. Eu sou a Jásperina, uma assistente virtual programada pelo Pedro Batista. Obrigado pela sua chamada. Neste momento, ainda não aprendi a responder automaticamente. Em breve, saberei fazê-lo. Adeus!"
  resp.say(msg, language="pt-PT", voice="alice")
  return str(resp)  


if __name__ == "__main__":
    app.run(debug=True)
