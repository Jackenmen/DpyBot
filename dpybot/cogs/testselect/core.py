import asyncio

import discord
from discord.ext import commands


class TestSelectView(discord.ui.View):
    @discord.ui.select(
        options=[
            discord.SelectOption(label="option 1"),
            discord.SelectOption(label="option 2"),
        ]
    )
    async def testselect(
        self, select: discord.ui.Select, interaction: discord.Interaction
    ) -> None:
        # Assigning to local would ensure we have a reference to the list
        # with the values selected in the interaction we're currently handling.
        values = select.values
        await interaction.response.defer()
        await asyncio.sleep(5)
        # select.values is whatever was sent in the last interaction
        # within last 5 seconds not the interaction we're currently handling
        # which is why we set a `values` local earlier
        await interaction.followup.send(
            f"{interaction.user.mention} selected {values!r}", ephemeral=True
        )


class TestSelect(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def testselect(self, ctx: commands.Context) -> None:
        await ctx.send("Some text", view=TestSelectView())
