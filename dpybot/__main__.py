import logging
import warnings

import discord
from discord.ext import commands

warnings.filterwarnings("default", category=DeprecationWarning)

bot = commands.AutoShardedBot(
    command_prefix=commands.when_mentioned_or("==="),
    intents=discord.Intents(members=True, presences=True),
)

logging.basicConfig(
    format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG,
)

log = logging.getLogger("dpybot")


@commands.is_owner()
@bot.command()
async def reload(ctx: commands.Context, cog_name: str) -> None:
    try:
        bot.reload_extension(f"dpybot.cogs.{cog_name}")
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
        bot.load_extension(f"dpybot.cogs.{cog_name}")
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
        bot.unload_extension(f"dpybot.cogs.{cog_name}")
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


if __name__ == "__main__":
    print(discord.__version__)
    TOKEN = ""
    bot.load_extension("dpybot.cogs.admin")
    try:
        bot.run(TOKEN)
    except discord.ConnectionClosed as e:
        if e.code == 4014:
            print(
                "You sent a disallowed intent for a Gateway Intent."
                " You may have tried to specify an intent"
                " that you have not enabled or are not whitelisted for."
            )
        else:
            raise
