import json
import logging

from discord.ext import commands

import modules
from modules import admin

with open('secret.json') as data_file:
    secret = json.load(data_file)
with open('config.json') as config:
    config = json.load(config)


logging.basicConfig(level=logging.INFO)

description = '''
Hihi! Im Atsuko, a bot made by Jackson Rakena in discord.py for general use in Discord.
View my source code: https://github.com/groundcontr0l/Atsuko
'''
bot = commands.Bot(
    command_prefix='+',
    description=description,
    pm_help=True
)

# Variables
modules = ['fun', 'admin', 'general']
api_modules = ['myanimelist']


# Ready event handler
@bot.event
async def on_ready():
    print('Logged in!')
    print('Username: ' + bot.user.name)
    print('ID: ' + bot.user.id)
    await load_all_modules()


async def load_all_modules():
    for module in modules:
        bot.load_extension(name="modules." + module)
        print('[Load All Modules]: Successfully loaded non-API module ' + module + '.')
    for api_module in api_modules:
        bot.load_extension(name="modules.api." + api_module)
        print('[Load All Modules]: Successfully loaded API module ' + api_module + '.')


async def unload_all_modules():
    for module in modules:
        bot.unload_extension(name="modules." + module)
        print('[Unload All Modules]: Successfully unloaded non-API module ' + module + '.')
    for api_module in api_modules:
        bot.unload_extension(name="modules.api." + api_module)
        print('[Unload All Modules]: Successfully unloaded API module ' + api_module + '.')


async def check_api_module(module):
    if module in api_modules:
        return True
    else:
        return False


@bot.command(pass_context=True)
async def reload(ctx, module_to_reload: str):
    """Reloads a certain module."""
    admin_instance = admin.admin(bot)
    if admin_instance.check_owner(ctx.message.author):
        if await check_api_module(module=module_to_reload):
            try:
                bot.unload_extension("modules.api." + module_to_reload)
                bot.load_extension("modules.api." + module_to_reload)
                await bot.say(":information_source: Successfully reloaded `" + module_to_reload + "`!")
                print("Reloaded " + module_to_reload + " successfully.")
            except ImportError:
                await bot.say(":warning: I could not find a module called `" + module_to_reload + "`.")
                print("Couldn't find " + module_to_reload + ", reload failed.")
        else:
            try:
                bot.unload_extension("modules." + module_to_reload)
                bot.load_extension("modules." + module_to_reload)
                await bot.say(":information_source: Successfully reloaded `" + module_to_reload + "`!")
                print("Reloaded " + module_to_reload + " successfully.")
            except ImportError:
                await bot.say(":warning: I could not find a module called `" + module_to_reload + "`.")
                print("Couldn't find " + module_to_reload + ", reload failed.")
    else:
        await bot.say(":warning: Insufficient permissions.")
        print("User " + ctx.message.author.name + " tried to execute a reload without permission.")


@bot.command(aliases=['sd'], pass_context=True)
async def sleep(ctx):
    """Shuts down the bot. [Bot Owner Only]"""
    admin_instance = admin.admin(bot)
    if admin.admin.check_owner(admin_instance, ctx.message.author):
        try:
            await unload_all_modules()
            await bot.say(":zzz: Going to sleep. Goodbye!")
            print("Sleep initiated.")
        except:
            await bot.say(":warning: Error sleeping.")
            print("Error sleeping.")
    else:
        await bot.say(":warning: Invalid permissions.")
        print("User " + ctx.message.author.name + " tried to sleep the bot without permission.")


@bot.command(aliases=['to'], pass_context=True)
async def awaken(ctx):
    """Awakens the bot after shutdown. [Bot Owner Only]"""
    admin_instance = admin.admin(bot)
    if admin.admin.check_owner(admin_instance, ctx.message.author):
        try:
            await load_all_modules()
            await bot.say(":sunny: Atsuko, awake and at your service!")
            print("Awoken.")
        except:
            await bot.say(":warning: Error waking up.")
            print("Error waking up.")
    else:
        await bot.say(":warning: Invalid permissions.")
        print("User " + ctx.message.author.name + " tried to awaken the bot without permission.")

bot.run(secret['token'])
