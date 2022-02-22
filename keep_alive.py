#do not execute this file if the bot is hosted in a docker or other similar environment

from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
  return "Flask Service Initialized"

def run():
  app.run(host='0.0.0.0', port=8080)

def keep_alive():
  t = Thread(target=run)
  t.start()
