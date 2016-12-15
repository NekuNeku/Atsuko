import discord
from discord.ext import commands
import random
import logging
import spice_api as spice
import requests
import xml.etree.ElementTree as ET
import json

with open('secret.json') as data_file:
    data = json.load(data_file)

logging.basicConfig(level=logging.INFO)

description = '''
A bot made by Jackson Rakena (aka groundcontrol) ^w^
'''

bot = commands.Bot(
    command_prefix='+',
    description=description
)


# Ready event handler
@bot.event
async def on_ready():
    print('Logged in!')
    print('Username: ' + bot.user.name)
    print('ID: ' + bot.user.id)


@bot.command(description='Bot test.', pass_context=True)
async def test(ctx, anime: str):
    """Test command."""
    auth = spice.init_auth("centralcommand", "$Wixoss04")
    search_results = spice.search(anime, spice.get_medium('anime'), auth)
    anime = discord.Embed()
    anime.title = search_results[0].title
    anime.type = "rich"
    descraw = search_results[0].synopsis
    descnoquot = descraw.replace("&quot;", '"')
    descnobr = descnoquot.replace("<br />", "\n")
    descnoi = descnobr.replace("[i]", "_")
    descnoit = descnoi.replace("[/i]", "_")
    descnodash = descnoit.replace("&#039;", "'")
    descnodash = descnodash.replace("&mdash;", "—")
    anime.description = descnodash
    await bot.send_message(ctx.message.channel, content=None, tts=False, embed=anime)


@bot.command(pass_context=True)
async def anitest(ctx, anime: str):
    search_req = anime.replace(" ", "+")
    page = requests.get("https://myanimelist.net/api/anime/search.xml?q=" + search_req, auth=("centralcommand", "$Wixoss04"))
    results = ET.fromstring(page.content.decode("utf-8"))
    anitest = discord.Embed()
    descraw = results[0].find("synopsis").text
    descnoquot = descraw.replace("&quot;", '"')
    descnobr = descnoquot.replace("<br />", "\n")
    descnoi = descnobr.replace("[i]", "_")
    descnoit = descnoi.replace("[/i]", "_")
    descnodash = descnoit.replace("&#039;", "'")
    descnodash = descnodash.replace("&mdash;", "—")
    anitest.description = descnodash
    anitest.title = results[0].find("title").text
    await bot.send_message(ctx.message.channel, embed=anitest)


@bot.command(description='We are Number One!')
async def wearenumberone():
    """Picks a random We Are Number One song/parody."""
    await bot.say(
        random.choice([
            "https://www.youtube.com/watch?v=oNVfrxkHj1M",
            "https://www.youtube.com/watch?v=AG8VFyW61e0",
            "https://www.youtube.com/watch?v=PfYnvDL0Qcw",
            "https://www.youtube.com/watch?v=Q2a5Lhl42r4",
            "https://www.youtube.com/watch?v=ju-F2JP9XcI",
            "https://www.youtube.com/watch?v=MDw9fAdO7-E",
            "https://www.youtube.com/watch?v=5SM4MBts9n4"
        ])
    )


@bot.command(description='Choose between two values.', pass_context=True)
async def choose(ctx, left: str, right: str):
    """Chooses between two values."""
    choose_embed = discord.Embed()
    choose_embed.title = "I pick..."
    choose_embed.type = "rich"
    choose_embed.description = random.choice([left, right])
    await bot.send_message(destination=ctx.message.channel, tts=False, content=None, embed=choose_embed)


@bot.command(description='Ping command.', pass_context=True)
async def ping(ctx):
    """Simple test."""
    pong = discord.Embed()
    pong.title = "Pong!"
    pong.type = "rich"
    await bot.send_message(destination=ctx.message.channel, content=None, tts=False, embed=pong)


@bot.command(description='Is the bot cool? Yes it is!', pass_context=True)
async def cool(ctx):
    """Checks if the bot is cool."""
    cool = discord.Embed()
    cool.title = "Is the bot cool?"
    cool.description = "Yes, the bot is _very_ cool. :sunglasses:"
    cool.type = "rich"
    await bot.send_message(destination=ctx.message.channel, content=None, tts=False, embed=cool)

bot.run(data['token'])
