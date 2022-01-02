import argparse
import asyncio
import logging
import os
import warnings

import discord
from dotenv import load_dotenv

from dpybot.bot import DpyBot

warnings.filterwarnings("default", category=DeprecationWarning)


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


def run_bot() -> None:
    TOKEN = os.environ["DPYBOT_TOKEN"]
    loop = asyncio.get_event_loop()
    bot = DpyBot()
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


def main() -> None:
    print("discord.py version:", discord.__version__)
    args = parse_cli_flags()
    load_dotenv()
    setup_logging(args.debug)
    run_bot()


if __name__ == "__main__":
    main()
