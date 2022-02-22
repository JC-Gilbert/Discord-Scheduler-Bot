import os
import importlib

async def cmdrun(client, message, prefix):
    cmd = message.content.split(' ')[0].split(prefix)[1]  
    args = message.content.split(cmd)[1][1:].split(' ')
    for filename in os.listdir('./commands'):
        if filename.endswith('.py'):
            imported = filename.split('.py')[0]
            mod = importlib.import_module(f'commands.{imported}')
            x = mod.name
            y = mod.aliases
            if x == cmd or cmd in y:
                await mod.run(client, message, args)