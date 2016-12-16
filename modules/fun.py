import random

import discord
from discord.ext import commands


class fun:
    """No Commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["wano"])
    async def wearenumberone(self):
        """Picks a random We Are Number One song/parody."""
        await self.bot.say(
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

    @commands.command(pass_context=True)
    async def cool(self, ctx):
        """Checks if the bot is cool."""
        cool = discord.Embed()
        cool.title = "Is the bot cool?"
        cool.description = "Yes, the bot is _very_ cool. :sunglasses:"
        cool.type = "rich"
        await self.bot.send_message(destination=ctx.message.channel, content=None, tts=False, embed=cool)


def setup(bot):
    n = fun(bot)
    bot.add_cog(n)
