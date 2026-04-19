import logging
from collections.abc import Callable
from typing import TypeVar

import discord
from discord import app_commands
from discord.ext import commands


T = TypeVar("T")
log = logging.getLogger(__name__)


def app_command_check(name: str) -> Callable[[T], T]:
    def predicate(interaction: discord.Interaction) -> bool:
        log.info("%r app command check called!", name)
        return True

    return app_commands.check(predicate)


def command_check(name: str) -> Callable[[T], T]:
    def predicate(ctx: commands.Context) -> bool:
        log.info("%r command check called!", name)
        return True

    return commands.check(predicate)


class MySubGroup1(app_commands.Group, name="subgroup1"):
    @app_command_check("/group-with-subgroup-subclass subgroup1 command")
    @app_commands.command(name="command")
    async def my_command(self, interaction: discord.Interaction) -> None:
        log.info("`/group-with-subgroup-subclass subgroup1 command` executing...")
        await interaction.response.send_message("Hello!")

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        log.info("`MySubGroup1.interaction_check()` called!")
        return True


class MySubGroup2(app_commands.Group, name="subgroup2"):
    @app_command_check("/groupcog subgroup2 command")
    @app_commands.command(name="command")
    async def my_command(self, interaction: discord.Interaction) -> None:
        log.info("`/groupcog subgroup2 command` executing...")
        await interaction.response.send_message("Hello!")

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        log.info("`MySubGroup2.interaction_check()` called!")
        return True


class MySubGroup3(app_commands.Group, name="subgroup3"):
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        log.info("`MySubGroup3.interaction_check()` called!")
        return True


class GroupWithSubGroupSubclass(
    app_commands.Group, name="group-with-subgroup-subclass"
):
    sub_group = MySubGroup1()

    @app_command_check("/group-with-subgroup-subclass command")
    @app_commands.command(name="command")
    async def my_command(self, interaction: discord.Interaction) -> None:
        log.info("`/group-with-subgroup-subclass command` executing...")
        await interaction.response.send_message("Hello!")

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        log.info("`GroupWithSubGroupSubclass.interaction_check()` called!")
        return True


class GroupWithSubGroup(app_commands.Group, name="group-with-subgroup"):
    sub_group = app_commands.Group(name="subgroup", description="desc")

    @app_command_check("/group-with-subgroup subgroup command")
    @sub_group.command(name="command")
    async def subgroup_command(self, interaction: discord.Interaction) -> None:
        log.info("`/group-with-subgroup subgroup command` executing...")
        await interaction.response.send_message("Hello!")

    @app_command_check("/group-with-subgroup command")
    @app_commands.command(name="command")
    async def my_command(self, interaction: discord.Interaction) -> None:
        log.info("`/group-with-subgroup command` executing...")
        await interaction.response.send_message("Hello!")

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        log.info("`GroupWithSubGroup.interaction_check()` called!")
        return True


async def my_group_cog_app_command_interaction_check(
    interaction: discord.Interaction,
) -> bool:
    log.info("`my_group_cog_app_command_interaction_check()` called!")
    return True


class MyGroupCog(commands.GroupCog, group_name="groupcog"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    sub_group3 = MySubGroup3()
    sub_group2 = MySubGroup2()
    sub_group = app_commands.Group(name="subgroup", description="desc")

    @app_command_check("/groupcog subgroup3 command")
    @sub_group3.command(name="command")
    async def subgroup3_command(self, interaction: discord.Interaction) -> None:
        log.info("`/groupcog subgroup3 command` executing...")
        await interaction.response.send_message("Hello!")

    @app_command_check("/groupcog subgroup command")
    @sub_group.command(name="command")
    async def subgroup_command(self, interaction: discord.Interaction) -> None:
        log.info("`/groupcog subgroup command` executing...")
        await interaction.response.send_message("Hello!")

    @app_command_check("/groupcog command")
    @app_commands.command(name="command")
    async def my_command(self, interaction: discord.Interaction) -> None:
        log.info("`/groupcog command` executing...")
        await interaction.response.send_message("Hello!")

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        # this won't run, when user runs /group subgroup command
        log.info("`MyGroupCog.interaction_check()` called!")
        return True

    @app_command_check("/groupcog hybridcommand")
    @command_check("/groupcog hybridcommand")
    @commands.hybrid_command(name="hybridcommand")
    async def my_hybrid_command(self, ctx: commands.Context) -> None:
        log.info("`/groupcog hybridcommand` executing...")
        await ctx.interaction.response.send_message("Hello!")

    @app_command_check("/groupcog hybridgroup")
    @command_check("/groupcog hybridgroup")
    @commands.hybrid_group(name="hybridgroup")
    async def my_hybrid_group(self, ctx: commands.Context) -> None:
        log.info("`/groupcog hybridgroup` executing...")
        await ctx.interaction.response.send_message("Hello!")

    @app_command_check("/groupcog hybridgroup command")
    @command_check("/groupcog hybridgroup command")
    @my_hybrid_group.command(name="subcommand")
    async def my_hybrid_group_subcommand(self, ctx: commands.Context) -> None:
        log.info("`/groupcog hybridgroup command` executing...")
        await ctx.interaction.response.send_message("Hello!")
