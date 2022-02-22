from datetime import datetime  
from datetime import timedelta  
from utils import build_role_lookup, add_member_role, notify, parse_int, schedule_team_join

name = 'join'
aliases = ['join']

async def run(client, message, args):
    team_name = ""
    duration_in_days = 60

    if not args[0]:
        message_content = 'You must specify a team to join.'
        await notify(message.channel, message.author, message_content)
        return

    if len(args) > 1:
        duration_in_days = await parse_int(message.channel, '', args[1])
        if duration_in_days == None:
          return

    requesting_member = message.author
    team_name = args[0]

    role_lookup = await build_role_lookup(message.guild.roles)
    user_roles_lookup = await build_role_lookup(message.author.roles)
    
    if team_name not in role_lookup:
        message_content = f'No eligible role matching **{team_name}** was found.'
        await notify(message.channel, message.author, message_content)
        return

    if team_name in user_roles_lookup:
        message_content = f'You already have a role matching **{team_name}**.'
        await notify(message.channel, message.author, message_content)
        return

    await add_member_role(requesting_member, role_lookup[team_name])
    await message.author.add_roles(role_lookup[team_name], reason=None, atomic=True)
    await schedule_team_join(message.guild.id, message.channel.id, requesting_member.id, datetime.now() + timedelta(seconds=duration_in_days), role_lookup[team_name].id)

    message_content = f'Assigning you to **{role_lookup[team_name].name}** for {str(duration_in_days)} day(s).'
    await notify(message.channel, message.author, message_content)