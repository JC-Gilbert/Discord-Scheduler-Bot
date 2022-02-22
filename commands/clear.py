from replit import db

name = 'clear'
aliases = ['clear']

async def run(client, message, args):
  db.clear()