import json
import logging
import random
import xml.etree.ElementTree as ET

import discord
import requests
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
    description=description
)


# Ready event handler
@bot.event
async def on_ready():
    print('Logged in!')
    print('Username: ' + bot.user.name)
    print('ID: ' + bot.user.id)


@bot.command(pass_context=True)
async def anime(ctx, *, anime_target: str):
    """Searches for an anime from MyAnimeList."""
    search_req = anime_target.replace(" ", "+")
    page = requests.get("https://myanimelist.net/api/anime/search.xml?q=" + search_req,
                        auth=(secret['MALUsername'], secret['MALPassword']))
    results = ET.fromstring(page.content.decode("utf-8"))
    anime_embed = discord.Embed()
    descraw = results[0].find("synopsis").text
    descnoquot = descraw.replace("&quot;", '"')
    descnobr = descnoquot.replace("<br />", "\n")
    descnoi = descnobr.replace("[i]", "_")
    descnoit = descnoi.replace("[/i]", "_")
    descnodash = descnoit.replace("&#039;", "'")
    descnodash = descnodash.replace("&mdash;", "—")
    descnodash = descnodash.replace("&rsquo;", "'")
    descfinal = descnodash.split("\n")
    anime_embed.description = descfinal[0]
    anime_embed.title = results[0].find("title").text + " (" + results[0].find("english").text + ")"
    anime_embed.url = "https://myanimelist.net/anime/" + results[0].find("id").text
    anime_embed.set_image(url=results[0].find("image").text)
    anime_embed.set_footer(text="All information provided by the MyAnimeList API",
                           icon_url="http://4.bp.blogspot.com/-lLUS5tswuGw/T5DyKdDDZPI/AAAAAAAACVU/N4dY03aXJNA/s1600/128.png")
    anime_embed.add_field(name="Status", value=results[0].find("status").text)
    anime_embed.add_field(name="Type", value=results[0].find("type").text)
    anime_embed.add_field(name="Start Date", value=results[0].find("start_date").text)
    anime_embed.add_field(name="End Date", value=results[0].find("end_date").text)
    await bot.send_message(ctx.message.channel, embed=anime_embed)


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


@bot.command(pass_context=True)
async def setgame(ctx, *, gamename: str):
    """Sets the bot's game."""
    if ctx.message.author.id == config['id']:
        gamea = discord.Game()
        gamea.name = gamename
        await bot.change_presence(game=gamea)
        await bot.say(":information_source: Changed game.")
    else:
        await bot.say(":warning: Cannot set game, invalid permissions.")


bot.run(secret['token'])
