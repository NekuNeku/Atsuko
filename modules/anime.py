import json
import xml.etree.ElementTree as ET

import discord
import requests
from discord.ext import commands


class anime:
    """Commands to get anime/manga from MyAnimeList."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def anime(self, ctx, *, anime_target: str):
        """Searches for an anime from MyAnimeList."""
        with open('secret.json') as data_file:
            secret = json.load(data_file)
        search_req = anime_target.replace(" ", "+")
        page = requests.get("https://myanimelist.net/api/anime/search.xml?q=" + search_req,
                            auth=(secret['MALUsername'], secret['MALPassword']))
        results = ET.fromstring(page.content.decode("utf-8"))
        anime_embed = discord.Embed()
        anime_embed.type = "rich"
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
        await self.bot.send_message(ctx.message.channel, embed=anime_embed)


def setup(bot):
    n = anime(bot)
    bot.add_cog(n)
