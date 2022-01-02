from discord.ext import commands

from .enums import Color


class SpecialColor(commands.Converter):
    async def convert(self, ctx: commands.Context, arg: str) -> Color:
        try:
            number = int(arg)
        except ValueError:
            raise commands.BadArgument(f"`{arg}` is not a valid number!")
        try:
            return Color(int(number))
        except ValueError:
            raise commands.BadArgument(f"We don't have a color with number `{number}`.")
