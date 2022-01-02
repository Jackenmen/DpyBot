import argparse
import asyncio
import logging
import os
import warnings

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

warnings.filterwarnings("default", category=DeprecationWarning)

bot = commands.AutoShardedBot(
    command_prefix=commands.when_mentioned_or("==="),
    intents=discord.Intents.all(),
)

log = logging.getLogger("dpybot")


def reload_extension(cog_name: str) -> None:
    try:
        bot.reload_extension(f"dpybot.ext_cogs.{cog_name}")
    except commands.ExtensionNotLoaded:
        bot.reload_extension(f"dpybot.cogs.{cog_name}")
    except commands.ExtensionNotFound:
        bot.load_extension(f"dpybot.cogs.{cog_name}")


def load_extension(cog_name: str) -> None:
    try:
        bot.load_extension(f"dpybot.ext_cogs.{cog_name}")
    except commands.ExtensionNotFound:
        bot.load_extension(f"dpybot.cogs.{cog_name}")


def unload_extension(cog_name: str) -> None:
    try:
        bot.unload_extension(f"dpybot.ext_cogs.{cog_name}")
    except commands.ExtensionNotLoaded:
        bot.unload_extension(f"dpybot.cogs.{cog_name}")


@commands.is_owner()
@bot.command()
async def reload(ctx: commands.Context, cog_name: str) -> None:
    try:
        reload_extension(cog_name)
    except commands.ExtensionNotLoaded:
        await ctx.send(f"Cog with name `{cog_name}` wasn't loaded.")
    except commands.ExtensionNotFound:
        await ctx.send(f"Can't find cog with name `{cog_name}.")
    except commands.NoEntryPointError:
        await ctx.send(f"Cog with name `{cog_name}` doesn't have `setup()` function.")
    except commands.ExtensionFailed as e:
        await ctx.send(f"Cog with name `{cog_name}` couldn't be reloaded. See logs for more details.")
        log.error("Cog with name `%s` couldn't be reloaded.", cog_name, exc_info=e.original)
    else:
        await ctx.send(f"{cog_name} reloaded.")


@commands.is_owner()
@bot.command()
async def load(ctx: commands.Context, cog_name: str) -> None:
    try:
        load_extension(cog_name)
    except commands.ExtensionAlreadyLoaded:
        await ctx.send(f"Cog with name `{cog_name}` is already loaded.")
    except commands.ExtensionNotFound:
        await ctx.send(f"Can't find cog with name `{cog_name}.")
    except commands.NoEntryPointError:
        await ctx.send(f"Cog with name `{cog_name}` doesn't have `setup()` function.")
    except commands.ExtensionFailed as e:
        await ctx.send(f"Cog with name `{cog_name}` couldn't be loaded. See logs for more details.")
        log.error("Cog with name `%s` couldn't be loaded.", cog_name, exc_info=e.original)
    else:
        await ctx.send(f"{cog_name} loaded.")


@commands.is_owner()
@bot.command()
async def unload(ctx: commands.Context, cog_name: str) -> None:
    try:
        unload_extension(cog_name)
    except commands.ExtensionNotLoaded:
        await ctx.send(f"Cog with name `{cog_name}` wasn't loaded.")
    else:
        await ctx.send(f"{cog_name} unloaded.")


@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError) -> None:
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send_help(ctx.command)
    elif isinstance(error, commands.BadArgument):
        if error.args:
            await ctx.send(error.args[0])
        else:
            await ctx.send_help(ctx.command)
    else:
        log.error(type(error).__name__, exc_info=error)


@bot.event
async def on_ready():
    log.info("I am ready!")


def parse_cli_flags() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--debug", action="store_true", help="Set the logger's level to debug."
    )
    return parser.parse_args()


def setup_logging(debug: bool = False) -> None:
    info_file_handler = logging.FileHandler("info.log", encoding="utf-8")
    debug_file_handler = logging.FileHandler("debug.log", mode="w", encoding="utf-8")
    stdout_handler = logging.StreamHandler()

    info_file_handler.setLevel(logging.INFO)
    if not debug:
        stdout_handler.setLevel(logging.INFO)

    logging.basicConfig(
        format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.DEBUG,
        handlers=[stdout_handler, info_file_handler, debug_file_handler],
    )


def _cancel_all_tasks(loop: asyncio.AbstractEventLoop) -> None:
    to_cancel = asyncio.all_tasks(loop)
    if not to_cancel:
        return

    for task in to_cancel:
        task.cancel()

    loop.run_until_complete(asyncio.gather(*to_cancel, return_exceptions=True))

    for task in to_cancel:
        if task.cancelled():
            continue
        if (exception := task.exception()) is not None:
            loop.call_exception_handler(
                {
                    "message": "unhandled exception during shutdown",
                    "exception": exception,
                    "task": task,
                }
            )


if __name__ == "__main__":
    print("discord.py version:", discord.__version__)
    args = parse_cli_flags()
    setup_logging(args.debug)
    TOKEN = os.getenv("DPYBOT_TOKEN")
    LOAD_ON_STARTUP = os.getenv("DPYBOT_LOAD_ON_STARTUP", "").split(",")
    for cog in LOAD_ON_STARTUP:
        load_extension(cog)

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(bot.start(TOKEN))
    except KeyboardInterrupt:
        print("Ctrl+C received, exiting...")
    except discord.PrivilegedIntentsRequired:
        print(
            "You sent a disallowed intent for a Gateway Intent."
            " You may have tried to specify an intent"
            " that you have not enabled or are not whitelisted for."
        )
    finally:
        try:
            loop.run_until_complete(bot.close())
            _cancel_all_tasks(loop)
            loop.run_until_complete(asyncio.sleep(2))
            loop.run_until_complete(loop.shutdown_asyncgens())
        finally:
            asyncio.set_event_loop(None)
            loop.close()
