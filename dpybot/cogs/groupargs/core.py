import discord
from discord.ext import commands


class GroupArgs(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def cogname(self, ctx):
        pass

    @cogname.group(invoke_without_command=True)
    async def edit(self, ctx, channel: discord.TextChannel):
        if ctx.invoked_subcommand is None:
            return
        ctx.some_special_attrname = channel

    @edit.group(name='name')
    async def edit_name(self, ctx):
        pass

    @edit_name.group(name='format')
    async def edit_name_format(self, ctx, option: str):
        await ctx.send(f"{ctx.some_special_attrname=}")
        await ctx.send(f"{option=}")
