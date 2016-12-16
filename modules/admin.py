import json

import discord
from discord.ext import commands


class admin:
    """No Commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['sg'], pass_context=True)
    async def setgame(self, ctx, *, gamename: str):
        """Sets the bot's game."""
        with open('config.json') as config:
            config = json.load(config)
        if ctx.message.author.id == config['id']:
            gamea = discord.Game()
            gamea.name = gamename
            await self.bot.change_presence(game=gamea)
            await self.bot.say(":information_source: Changed game.")
        else:
            await self.bot.say(":warning: Cannot set game, invalid permissions.")


def setup(bot):
    n = admin(bot)
    bot.add_cog(n)
