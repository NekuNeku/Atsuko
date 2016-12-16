import random

import discord
from discord.ext import commands


class general:
    """No Commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='Choose between two values.', pass_context=True)
    async def choose(self, ctx, left: str, right: str):
        """Chooses between two values."""
        choose_embed = discord.Embed()
        choose_embed.title = "I pick..."
        choose_embed.type = "rich"
        choose_embed.description = random.choice([left, right])
        await self.bot.send_message(destination=ctx.message.channel, tts=False, content=None, embed=choose_embed)

    @commands.command(description='Ping command.', pass_context=True)
    async def ping(self, ctx):
        """Simple test."""
        pong = discord.Embed()
        pong.title = "Pong!"
        pong.type = "rich"
        await self.bot.send_message(destination=ctx.message.channel, content=None, tts=False, embed=pong)


def setup(bot):
    n = general(bot)
    bot.add_cog(n)
