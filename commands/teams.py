from utils import role_key

name = 'teams'
aliases = ['teams']

async def run(client, message, args):
    role_display = []
    roles = message.guild.roles

    for role in roles:
        if role.name.startswith(role_key):
            role_display.append(role.name)

    role_display = list(reversed(role_display))

    await message.channel.send('**Teams available to join: **' + ', '.join(role_display))