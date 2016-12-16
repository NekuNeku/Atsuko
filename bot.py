import json
import logging

from discord.ext import commands

from modules import admin

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


@bot.command()
async def reload(cog_to_reload: str):
    """Reloads a certain cog."""
    try:
        bot.unload_extension("modules." + cog_to_reload)
        bot.load_extension("modules." + cog_to_reload)
        await bot.say(":information_source: Successfully reloaded `" + cog_to_reload + "`!")
    except ImportError as e:
        await bot.say(":warning: I cannot find a module called `" + cog_to_reload + "`.")
        print(e)


@bot.command(pass_context=True)
async def load(ctx, cog_to_load: str):
    """Loads a certain cog."""
    admin_instance = admin.admin(bot)
    if admin.admin.check_owner(admin_instance, member=ctx.message.author):
        try:
            bot.load_extension("modules." + cog_to_load)
            await bot.say(":information_source: Successfully loaded `" + cog_to_load + "`!")
        except Exception as e:
            await bot.say(":warning: Cannot load `" + cog_to_load + "`. It may not exist.")
            print(e)
    else:
        await bot.say(":warning: Invalid permissions.")


@bot.command(pass_context=True)
async def unload(ctx, cog_to_unload: str):
    """Unloads a certain cog."""
    admin_instance = admin.admin(bot)
    if admin.admin.check_owner(admin_instance, member=ctx.message.author):
        bot.unload_extension("modules." + cog_to_unload)
        await bot.say(":information_source: Attempted to unload `" + cog_to_unload + "`!")
    else:
        await bot.say(":warning: Invalid permissions.")

bot.run(secret['token'])
