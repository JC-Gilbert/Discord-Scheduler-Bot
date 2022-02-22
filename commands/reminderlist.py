from replit import db
from utils import notify, split_token
from datetime import datetime
from dateutil import tz

name = 'reminderlist'
aliases = ['reminderlist']

async def run(client, message, args):
  reminders_list = []

  if "reminders" in db.keys():
    reminders = db["reminders"]

    for index in range(len(reminders)):
      expanded_reminder = reminders[index].split(split_token)

      guild = client.get_guild(int(expanded_reminder[0]))
      channel = guild.get_channel(int(expanded_reminder[1]))
      target_user = guild.get_member(int(expanded_reminder[2]))
      target_time = expanded_reminder[3]
      target_message = str(" ".join(expanded_reminder[4:]))

      #convert the reminder target_time to a EST format
      from_zone = tz.gettz('UTC')
      to_zone = tz.gettz('America/New_York')
      utc = datetime.strptime(str(target_time), '%Y-%m-%d %H:%M:%S.%f')
      utc = utc.replace(tzinfo=from_zone)
      local_time = utc.astimezone(to_zone)
      formatted_time = local_time.strftime("%b %d %Y at %I:%M:%S %p (%Z)")

      # if target_user == message.author:
      reminders_list.append(f'{index}: {channel}, {target_user}, {formatted_time}, {target_message}')
  
  if len(reminders_list) == 0:
    reminders_list.append('You have no reminders')

  await notify(message.channel, '', '\n'.join(reminders_list))