from discord.ext import commands

from .core import (
    GroupWithSubGroup,
    GroupWithSubGroupSubclass,
    MyGroupCog,
    my_group_cog_app_command_interaction_check,
)


async def setup(bot: commands.Bot) -> None:
    cog = MyGroupCog(bot)
    cog.app_command.interaction_check = my_group_cog_app_command_interaction_check
    await bot.add_cog(cog)
    bot.tree.add_command(GroupWithSubGroupSubclass())
    bot.tree.add_command(GroupWithSubGroup())
