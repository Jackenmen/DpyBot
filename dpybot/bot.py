import os

import discord
from discord.ext import commands

from dpybot import log
from dpybot.core_commands import Core


class DpyBot(commands.AutoShardedBot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix=commands.when_mentioned_or(
                os.getenv("DPYBOT_PREFIX", "===")
            ),
            intents=discord.Intents.all(),
        )

        LOAD_ON_STARTUP = os.getenv("DPYBOT_LOAD_ON_STARTUP", "").split(",")
        self.add_cog(Core(self))
        for pkg_name in LOAD_ON_STARTUP:
            self.load_package(pkg_name)

    async def on_ready(self) -> None:
        log.info("I am ready!")

    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ) -> None:
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send_help(ctx.command)
        elif isinstance(error, commands.BadArgument):
            if error.args:
                await ctx.send(error.args[0])
            else:
                await ctx.send_help(ctx.command)
        else:
            log.error(type(error).__name__, exc_info=error)

    def reload_package(self, name: str) -> None:
        try:
            self.reload_extension(f"dpybot.ext_cogs.{name}")
        except commands.ExtensionNotLoaded:
            self.reload_extension(f"dpybot.cogs.{name}")
        except commands.ExtensionNotFound:
            self.load_extension(f"dpybot.cogs.{name}")

    def load_package(self, name: str) -> None:
        try:
            self.load_extension(f"dpybot.ext_cogs.{name}")
        except commands.ExtensionNotFound:
            self.load_extension(f"dpybot.cogs.{name}")

    def unload_package(self, name: str) -> None:
        try:
            self.unload_extension(f"dpybot.ext_cogs.{name}")
        except commands.ExtensionNotLoaded:
            self.unload_extension(f"dpybot.cogs.{name}")
