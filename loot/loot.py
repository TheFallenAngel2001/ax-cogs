import discord

from discord.ext import commands

from redbot.core import Config
from redbot.core.bot import Red


class Loot:

    default_guild_settings = {

    }

    def __init__(self, bot: Red):
        self.bot = bot
        self._loot = Config.get_conf(self, 9741981201)

        self._loot.register_guild(**self.default_guild_settings)

    @commands.group(pass_context=True)
    async def loot(self, ctx):
        """Loot related commands"""
        if ctx.invoked_subcommand is None:
            await ctx.send_help()

    @loot.command(pass_context=True)
    async def add(self, ctx, name: str, char: str, price: int):
        """Adds players and amounts paid to an item"""
        name = name.lower()
        guild = ctx.guild
        loot = await self._loot.guild(guild).all()
        if name not in loot:
            await ctx.send("item doesn't exist, please use [p]loot create first")
            return
        loot[name][char] = price
        await ctx.send("{} paid {} for {}".format(char, price, name))
        await self._loot.guild(guild).set(loot)

    @loot.command(pass_context=True)
    async def create(self, ctx, name: str):
        """Creates an item in the current guild."""
        name = name.lower()
        guild = ctx.guild
        loot = await self._loot.guild(guild).all()
        if name in loot:
            await ctx.send("Item already exists, use another name.")
            return
        loot[name] = {}
        await ctx.send("{} has been added.".format(name))
        await self._loot.guild(guild).set(loot)

    @loot.command(pass_context=True)
    async def info(self, ctx, *name: str):
        """Shows who has invested in the item"""
        name = name.lower()
        guild = ctx.guild
        loot = await self._loot.guild(guild).all()
        if name not in loot.keys():
            await ctx.send("Please make sure that the name is spelled correctly and "
                           "that you can find it in [p]loot list")
            return
        players = "\n".join(list(loot[name].keys()))
        gold = "\n".join(str(x) for x in list(loot[name].values()))
        embed = discord.Embed(color=6465603)
        embed.set_author(name=name)
        embed.add_field(name="__Players__", value=players)
        embed.add_field(name="__Price Paid__", value=gold)
        await ctx.send(embed=embed)

    @loot.command(pass_context=True)
    async def list(self, ctx):
        """Shows existing loot in the current guild"""
        guild = ctx.guild
        loot = await self._loot.guild(guild).all()
        if len(loot) < 1:
            await ctx.send("No items have been created for this guild yet, please create some using [p]item create"
                           " first, thanks")
            return
        items = loot.keys()
        await ctx.send("Here are this guild's items:\n{}".format("\n".join(items)))

    @loot.command(pass_context=True, hidden=True)
    async def remove(self, ctx, name: str, char: str=None):
        """Deletes existing characters in an item or items"""
        name = name.lower()
        guild = ctx.guild
        loot = await self._loot.guild(guild).all()
        if name not in loot:
            await ctx.send("Please make sure that the name is spelled correctly and "
                           "that you can find it in [p]loot list")
            return
        if char is None:
            del loot[name]
        elif char in loot[name]:
            del loot[name][char]
        await ctx.send("{} has been removed".format(char if char else name))
        await self._loot.guild(guild).set(loot)
