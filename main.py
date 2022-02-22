import command
import discord
import os
from discord.ext import commands, tasks
from utils import check_reminders, check_teamjoins
from datetime import datetime
# from keep_alive import keep_alive

intents = discord.Intents.default()
intents.members = True

# init values
prefix = '$'
heartbeat_interval = 5

client = commands.Bot(command_prefix = prefix, intents=intents)

#task loop for the heartbeat
@tasks.loop(seconds=heartbeat_interval)
async def heartbeat():
  await check_reminders(client, datetime.now())
  await check_teamjoins(client, datetime.now())

#onready fires when bot starts
@client.event
async def on_ready():
  print('Bot is ready.')
  # keep_alive()
  heartbeat.start()

#when messages are received
@client.event
async def on_message(message):
  # if message.channel.type.name == 'private': return
  if message.author.bot: return
  if message.content.startswith(prefix) == False: return

  await command.cmdrun(client, message, prefix)

client.run(os.getenv('TOKEN'))