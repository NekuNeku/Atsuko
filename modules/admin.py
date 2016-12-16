import json

import discord
from discord.ext import commands


class admin:
    """This is a category for administrator [Bot Owner] commands."""

    def __init__(self, bot):
        self.bot = bot

    def check_owner(self, member: discord.Member):
        with open('config.json') as config:
            config = json.load(config)
        if member.id != config['id']:
            return False
        else:
            return True

    @commands.command(aliases=['sg'], pass_context=True)
    async def setgame(self, ctx, *, gamename: str):
        """Sets the bot's game. [Bot Owner Only]"""
        if self.check_owner(ctx.message.author):
            gamea = discord.Game()
            gamea.name = gamename
            await self.bot.change_presence(game=gamea)
            await self.bot.say(":information_source: Changed game to `Playing " + gamename + "`!")
        else:
            await self.bot.say(":warning: Invalid permissions.")


def setup(bot):
    n = admin(bot)
    bot.add_cog(n)
