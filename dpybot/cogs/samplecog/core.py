from discord.ext import commands

from .converters import SpecialColor
from .enums import Color


def mehhh(ctx):
    return False


class SampleCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def sendcolor(self, ctx: commands.Context, color: SpecialColor) -> None:
        if color == Color.red:
            await ctx.send("You chose the best color, red!")
        else:
            await ctx.send(f"You chose {color.name}!")

    @commands.check(mehhh)
    @commands.guild_only()
    @commands.group(invoke_without_command=True)
    async def blah(self, ctx: commands.Context) -> None:
        await ctx.send("blah")

    @blah.command()
    async def ah(self, ctx: commands.Context) -> None:
        await ctx.send("blah ah")
