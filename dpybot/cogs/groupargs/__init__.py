from discord.ext import commands

from .core import GroupArgs


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(GroupArgs(bot))
