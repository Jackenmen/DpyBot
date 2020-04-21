from discord.ext import commands

from .core import SampleCog


def setup(bot: commands.Bot) -> None:
    bot.add_cog(SampleCog(bot))
