from __future__ import annotations

from typing import TYPE_CHECKING

from discord.ext import commands

from dpybot import log

if TYPE_CHECKING:
    from dpybot.bot import DpyBot


class Core(commands.Cog):
    def __init__(self, bot: DpyBot) -> None:
        self.bot = bot

    @commands.is_owner()
    @commands.command()
    async def reload(self, ctx: commands.Context, pkg_name: str) -> None:
        try:
            await self.bot.reload_package(pkg_name)
        except commands.ExtensionNotLoaded:
            await ctx.send(f"Cog package with name `{pkg_name}` wasn't loaded.")
        except commands.ExtensionNotFound:
            await ctx.send(f"Can't find cog package with name `{pkg_name}.")
        except commands.NoEntryPointError:
            await ctx.send(
                f"Cog package with name `{pkg_name}` doesn't have `setup()` function."
            )
        except commands.ExtensionFailed as e:
            await ctx.send(
                f"Cog package with name `{pkg_name}` couldn't be reloaded."
                " See logs for more details."
            )
            log.error(
                "Cog package with name `%s` couldn't be reloaded.",
                pkg_name,
                exc_info=e.original,
            )
        else:
            await ctx.send(f"{pkg_name} reloaded.")

    @commands.is_owner()
    @commands.command()
    async def load(self, ctx: commands.Context, pkg_name: str) -> None:
        try:
            await self.bot.load_package(pkg_name)
        except commands.ExtensionAlreadyLoaded:
            await ctx.send(f"Cog package with name `{pkg_name}` is already loaded.")
        except commands.ExtensionNotFound:
            await ctx.send(f"Can't find cog package with name `{pkg_name}.")
        except commands.NoEntryPointError:
            await ctx.send(
                f"Cog package with name `{pkg_name}` doesn't have `setup()` function."
            )
        except commands.ExtensionFailed as e:
            await ctx.send(
                f"Cog package with name `{pkg_name}` couldn't be loaded."
                " See logs for more details."
            )
            log.error(
                "Cog package with name `%s` couldn't be loaded.",
                pkg_name,
                exc_info=e.original,
            )
        else:
            await ctx.send(f"{pkg_name} loaded.")

    @commands.is_owner()
    @commands.command()
    async def unload(self, ctx: commands.Context, pkg_name: str) -> None:
        try:
            await self.bot.unload_package(pkg_name)
        except commands.ExtensionNotLoaded:
            await ctx.send(f"Cog package with name `{pkg_name}` wasn't loaded.")
        else:
            await ctx.send(f"{pkg_name} unloaded.")

    @commands.command()
    async def ping(self, ctx: commands.Context) -> None:
        await ctx.send("Pong!")

    @commands.is_owner()
    @commands.command()
    async def shutdown(self, ctx: commands.Context) -> None:
        print("Shutting down...")
        await ctx.send("Shutting down...")
        await self.bot.close()
