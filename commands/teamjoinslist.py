from replit import db
from utils import notify, split_token
from datetime import datetime
from dateutil import tz

name = 'teamjoinslist'
aliases = ['teamjoinslist']
  
async def run(client, message, args):
  teamjoins_list = []

  if "teamjoins" in db.keys():
    teamjoins = db["teamjoins"]

    for index in range(len(teamjoins)):
      expanded_teamjoin = teamjoins[index].split(split_token)

      target_guild = client.get_guild(int(expanded_teamjoin[0]))
      target_channel = target_guild.get_channel(int(expanded_teamjoin[1]))
      target_user = target_guild.get_member(int(expanded_teamjoin[2]))
      target_time = expanded_teamjoin[3]
      target_role = target_guild.get_role(int(expanded_teamjoin[4]))

      #convert the reminder target_time to a EST format
      from_zone = tz.gettz('UTC')
      to_zone = tz.gettz('America/New_York')
      utc = datetime.strptime(str(target_time), '%Y-%m-%d %H:%M:%S.%f')
      utc = utc.replace(tzinfo=from_zone)
      local_time = utc.astimezone(to_zone)
      formatted_time = local_time.strftime("%b %d %Y at %I:%M:%S %p (%Z)")

      # if target_user == message.author:
      teamjoins_list.append(f'{index}: {target_channel}, {target_user}, {formatted_time}, {target_role}')

  if len(teamjoins_list) == 0:
    teamjoins_list.append('You have not joined any teams')

  await notify(message.channel, '', '\n'.join(teamjoins_list))