from discord.ext import commands

from .core import SampleCog


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(SampleCog(bot))
