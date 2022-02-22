from utils import build_role_lookup, notify, remove_member_role, split_token
from replit import db

name = 'leave'
aliases = ['leave']

async def run(client, message, args):
    if not args[0]:
        message_content = 'You must specify a team to leave.'
        await notify(message.channel, message.author, message_content)
        return

    team_name = args[0]
    teamjoins = []

    role_lookup = await build_role_lookup(message.guild.roles)
    user_roles_lookup = await build_role_lookup(message.author.roles)

    if team_name not in role_lookup:
        message_content = f'No eligible role matching {team_name} was found.'
        await notify(message.channel, message.author, message_content)
        return

    if team_name not in user_roles_lookup:
        message_content = f'You do not have a role matching {team_name}.'
        await notify(message.channel, message.author, message_content)
        return
    
    index = None
    team_match_index = None

    if "teamjoins" in db.keys():
      teamjoins = db["teamjoins"]

    if len(teamjoins) == 0:
      return
    else:
      for index in range(len(teamjoins)):
        expanded_reminder = teamjoins[index].split(split_token)

        target_guild = client.get_guild(int(expanded_reminder[0]))
        target_user = target_guild.get_member(int(expanded_reminder[2]))
        target_role = target_guild.get_role(int(expanded_reminder[4]))  

        if target_user == message.author and int(role_lookup[team_name].id) == int(target_role.id):
          team_match_index = index

      if team_match_index != None:
        await remove_member_role(message.author, role_lookup[team_name])
        del teamjoins[team_match_index]
        db["teamjoins"] = teamjoins
        await notify(message.channel, message.author, f'Removing you from {team_name}')














#     team_name = ""

#     if not args[0]:
#         message_content = 'You must specify a team to leave.'
#         await notify(message.channel, message.author, message_content)
#         return

#     team_name = args[0]

#     role_lookup = await build_role_lookup(message.guild.roles)
#     user_roles_lookup = await build_role_lookup(message.author.roles)

#     if team_name not in role_lookup:
#         message_content = f'No eligible role matching {team_name} was found.'
#         await notify(message.channel, message.author, message_content)
#         return

#     if team_name not in user_roles_lookup:
#         message_content = f'You do not have a role matching {team_name}.'
#         await notify(message.channel, message.author, message_content)
#         return

#     await remove_member_role(message.author, role_lookup[team_name])
#     await schedule_team_join(utils.role_action_type_id, message.guild.id, message.channel.id, message.author.id, role_lookup[team_name].id, None, False)

#     message_content = f'Removing you from **{role_lookup[team_name].name}**.'
#     await notify(message.channel, message.author, message_content)