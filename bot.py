import json
import logging

from discord.ext import commands

with open('secret.json') as data_file:
    secret = json.load(data_file)
with open('config.json') as config:
    config = json.load(config)


logging.basicConfig(level=logging.INFO)

description = '''
A bot made by Jackson Rakena (aka groundcontrol) ^w^
'''

bot = commands.Bot(
    command_prefix='+',
    description=description,
    pm_help=True
)


# Ready event handler
@bot.event
async def on_ready():
    print('Logged in!')
    print('Username: ' + bot.user.name)
    print('ID: ' + bot.user.id)
    bot.load_extension("modules.anime")
    bot.load_extension("modules.fun")
    bot.load_extension("modules.admin")
    bot.load_extension("modules.general")


bot.run(secret['token'])
