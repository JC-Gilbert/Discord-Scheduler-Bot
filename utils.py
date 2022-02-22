from replit import db
from datetime import datetime  
from datetime import timedelta  

#init globals
split_token = '|%$-%$|'
role_key = 'Team'
# reminder_action_type_id = 1
# guest_action_type_id = 2

#helper function to notify user
async def notify(channel, user, message_content):
  if user != None and user != "":
    await channel.send(f'{user.mention}: {message_content}')
  else:
    await channel.send(message_content)

#helper function to parse integer
async def parse_int(channel, user, i):
  try:
      return int(i)
  except:
      await notify(channel, user, 'You have specified an invalid numeric value, format, or index.')

#helper function to parse time
async def parse_time(message, time_string):
  time_now = datetime.now()
  time_offset = time_now

  if "d" in time_string:
    split_time = time_string.split("d")
    days = await parse_int(message.channel, message.author, split_time[0])
    if days == None:
      return
    time_offset = time_offset + timedelta(days=days)
    time_string = split_time[1]

  if "h" in time_string:
    split_time = time_string.split("h")
    hours = await parse_int(message.channel, message.author, split_time[0])
    if hours == None:
       return
    time_offset = time_offset + timedelta(hours=hours)
    time_string = split_time[1]

  if "m" in time_string:
    split_time = time_string.split("m")
    minutes = await parse_int(message.channel, message.author, split_time[0])
    if minutes == None:
      return
    time_offset = time_offset + timedelta(minutes=minutes)
    time_string = split_time[1]

  if "s" in time_string:
    split_time = time_string.split("s")
    seconds = await parse_int(message.channel, message.author, split_time[0])
    if seconds == None:
      return
    time_offset = time_offset + timedelta(seconds=seconds)
    time_string = split_time[1]

  return_val = None
  if time_offset != time_now:
    return_val = time_offset

  return return_val

#schedule a reminder
async def schedule_reminder(guild_id, channel_id, user_id, target_time, message):
  record = f'{guild_id}{split_token}{channel_id}{split_token}{user_id}{split_token}{target_time}{split_token}{message}'

  if "reminders" in db.keys():
    reminders = db["reminders"]
    reminders.append(record)
    db["reminders"] = reminders
  else:
    db["reminders"] = [record]

  reminders = db["reminders"]

#check reminders to issue a notification
async def check_reminders(client, time_now):
  reminders = []
  if "reminders" in db.keys():
    reminders = db["reminders"]

  if len(reminders) == 0:
    return
  else:
    for index in range(len(reminders)):
      expanded_reminder = reminders[index].split(split_token)

      target_guild = client.get_guild(int(expanded_reminder[0]))
      target_channel = target_guild.get_channel(int(expanded_reminder[1]))
      target_user = target_guild.get_member(int(expanded_reminder[2]))
      target_time = expanded_reminder[3]
      target_message = str(" ".join(expanded_reminder[4:]))

      if (str(time_now) > target_time):
        if target_channel != None and target_user != None and target_message != None:
          # await notify(target_channel, target_user, target_message)
          await notify(target_channel, '', target_message)
          
        del reminders[index]
        db["reminders"] = reminders

#helpers for role things
async def build_role_lookup(roles):
    roles_lookup = {}

    for role in roles:
        if role.name.startswith(role_key):
            roles_lookup[role.name] = role

    return roles_lookup

async def add_member_role(requesting_member, role):
    await requesting_member.add_roles(role, reason=None, atomic=True)

async def remove_member_role(requesting_member, role):
    await requesting_member.remove_roles(role, reason=None, atomic=True)

async def schedule_team_join(guild_id, channel_id, user_id, target_time, role_id):
  record = f'{guild_id}{split_token}{channel_id}{split_token}{user_id}{split_token}{target_time}{split_token}{role_id}'

  if "teamjoins" in db.keys():
    teamjoins = db["teamjoins"]
    teamjoins.append(record)
    db["teamjoins"] = teamjoins
  else:
    db["teamjoins"] = [record]

  teamjoins = db["teamjoins"]

async def check_teamjoins(client, time_now):
  teamjoins = []
  if "teamjoins" in db.keys():
    teamjoins = db["teamjoins"]

  if len(teamjoins) == 0:
    return
  else:
    for index in range(len(teamjoins)):
      expanded_reminder = teamjoins[index].split(split_token)

      target_guild = client.get_guild(int(expanded_reminder[0]))
      target_channel = target_guild.get_channel(int(expanded_reminder[1]))
      target_user = target_guild.get_member(int(expanded_reminder[2]))
      target_time = expanded_reminder[3]
      target_role = target_guild.get_role(int(expanded_reminder[4]))

      if (str(time_now) > target_time):
        if (target_channel != None and target_user != None and target_role != None):
            message_content = f"Removing you from **{target_role}**."
            await notify(target_channel, target_user, message_content)                        

            for role in target_user.roles:
              if int(role.id) == int(target_role.id):
                await remove_member_role(target_user, target_role)
                
        del teamjoins[index]
        db["teamjoins"] = teamjoins