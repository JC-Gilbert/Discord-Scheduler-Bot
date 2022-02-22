from replit import db
from utils import notify, parse_int, split_token

name = 'delete'
aliases = ['delete']

async def run(client, message, args):
  if "reminders" in db.keys():
    reminders = db["reminders"]

  index = await parse_int(message.channel, message.author, args[0])
  if index == None:
    return

  if len(reminders) > index:
    expanded_reminder = reminders[index].split(split_token)

    guild = client.get_guild(int(expanded_reminder[0]))
    target_user = guild.get_member(int(expanded_reminder[2]))

    # if target_user == message.author:
    del reminders[index]
    db["reminders"] = reminders
    await notify(message.channel, message.author, 'Reminder deleted')
    # else:
    #   await notify(message.channel, message.author, 'You may only deleted your own reminders')
  else:
    await notify(message.channel, message.author, "That is not a valid index")