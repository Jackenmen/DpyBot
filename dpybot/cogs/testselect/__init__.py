from discord.ext import commands

from .core import TestSelect


def setup(bot: commands.Bot) -> None:
    bot.add_cog(TestSelect(bot))
