from discord.ext import commands

from .core import GroupArgs


def setup(bot: commands.Bot) -> None:
    bot.add_cog(GroupArgs(bot))
