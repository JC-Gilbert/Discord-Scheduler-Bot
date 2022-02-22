from utils import schedule_reminder, notify, parse_int 
from datetime import datetime  
from datetime import timedelta  

name = 'remind'
aliases = ['remind']
error_msg = '''You must specify both a time and message.
    ex: 6d10h2m5s Message goes here'''

async def run(client, message, args):
    if len(args) < 2:
        await notify(message.channel, message.author, error_msg)
        return

    reminder_time = args[0]
    reminder_message = str(" ".join(args[1:]))
    time_offset = datetime.now()
    days = ""
    hours = ""
    minutes = ""
    seconds = ""
    contained_time_parse = False

    if "d" in reminder_time:
        split_time = reminder_time.split("d")
        days = await parse_int(message.channel, message.author, split_time[0])
        if days == None:
          return
        if days > 6:
          await notify(message.channel, message.author, 'Reminders must be set for less than 7 days')
          return
        time_offset = time_offset + timedelta(days=days)
        reminder_time = split_time[1]
        contained_time_parse = True

    if "h" in reminder_time:
      split_time = reminder_time.split("h")
      hours = await parse_int(message.channel, message.author, split_time[0])
      if hours == None:
          return
      if hours > 23:
          await notify(message.channel, message.author, 'Use days for 24 or more hours')
          return
      time_offset = time_offset + timedelta(hours=hours)
      reminder_time = split_time[1]
      contained_time_parse = True

    if "m" in reminder_time:
        split_time = reminder_time.split("m")
        minutes = await parse_int(message.channel, message.author, split_time[0])
        if minutes == None:
            return
        if minutes > 59:
          await notify(message.channel, message.author, 'Use hours for 60 or more minutes')
          return
        time_offset = time_offset + timedelta(minutes=minutes)
        reminder_time = split_time[1]
        contained_time_parse = True

    if "s" in reminder_time:
        split_time = reminder_time.split("s")
        seconds = await parse_int(message.channel, message.author, split_time[0])
        if seconds == None:
            return
        if seconds > 59:
          await notify(message.channel, message.author, 'Use minutes for 60 or more seconds')
          return
        time_offset = time_offset + timedelta(seconds=seconds)
        reminder_time = split_time[1]
        contained_time_parse = True

    if contained_time_parse == False:
        await notify(message.channel, message.author, error_msg)
        return

    await notify(message.channel, message.author, 'Alright, reminder set!')
    await schedule_reminder(message.guild.id, message.channel.id, message.author.id, time_offset, reminder_message)