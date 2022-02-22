#do not execute this file if you are hosting your own bot in a docker or other environment

from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
  return "Hello. I'm doing the thing!"

def run():
  app.run(host='0.0.0.0', port=8080)

def keep_alive():
  t = Thread(target=run)
  t.start()
