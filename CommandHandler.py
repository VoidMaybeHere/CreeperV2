from discord.ext import commands
import discord
import commandLibrary as c
from logHandler import logHandler

logger = logHandler.genLogger(logHandler, logName="CommandHandler")

def register_commands(bot: commands.Bot):
    @bot.tree.command(name="stats", description="Returns the stats of a specific user")
    @discord.app_commands.describe(user="Discord user", word="Tracked word")
    async def getStats(ctx: discord.Interaction, user: discord.User = None, word: str = None):
        if user is None:
            await ctx.response.send_message(c.getServerStats(ctx.guild, logger=logger), ephemeral=True)
            return
        if word is None:
            await ctx.response.send_message(c.getAllStats(ctx.guild, user,logger=logger), ephemeral=True)
            return
        word = word.lower()
        await ctx.response.send_message(f"{user.mention} has said {word} {c.getStat(ctx.guild, user, word)} times.", ephemeral=True)
        return

    @bot.tree.command(name="track", description="Track a word and give a response")
    @commands.has_permissions(manage_guild=True)
    @discord.app_commands.describe(word="Word to track", response="Response to give, if any")
    async def addWord(ctx: discord.Interaction, word: str, response: str = None):
        await ctx.response.send_message(c.trackWord(ctx, word, response), ephemeral=True)
        return

    @bot.tree.command(name="untrack", description="Untrack a word, if it exists")
    @commands.has_permissions(manage_guild=True)
    @discord.app_commands.describe(word="Word to untrack")
    async def removeWord(ctx: discord.Interaction, word: str):
        await ctx.response.send_message(c.untrackWord(ctx, word), ephemeral=True)
        return


