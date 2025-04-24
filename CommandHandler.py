from bot import bot
import discord
import commandLibrary as c


@bot.tree.command(name="stats", description="Returns the stats of a specific user")
@discord.app_commands.describe(user = "Discord user", word = "Tracked word")
async def getStats(ctx : discord.Interaction, user: discord.User=None, word: str=None): # Gets the stats of a user for s specific word, all words for a user, or all stats for a server
    if user == None:
        await ctx.response.send_message(c.getServerStats(ctx.guild), ephemeral=True)
        return
    if word == None:
        await ctx.response.send_message(c.getAllStats(ctx.guild, user), ephemeral=True)
        return
    word = word.lower()
    await ctx.response.send_message(f"{user.mention} has said {word} {c.getStat(ctx.guild, user, word)} times.", ephemeral=True)
    return
    
@bot.tree.command(name="track", description="Track a word and give a response")
@discord.ext.commands.has_permissions(manage_guild=True)
@discord.app_commands.describe(word = "Word to track", response = "Response to give, if any")
async def addWord(ctx: discord.Interaction, word: str, response: str=None): # Adds a word to the tracked words dict
    await ctx.response.send_message(c.trackWord(ctx,word,response), ephemeral=True)
    return

@bot.tree.command(name="untrack", description="Untrack a word, if it exists")
@discord.ext.commands.has_permissions(manage_guild=True)
@discord.app_commands.describe(word = "Word to untrack")
async def removeWord(ctx: discord.Interaction, word: str): # Removes a word from the tracked words dict
    await ctx.response.send_message(c.untrackWord(ctx,word), ephemeral=True)
    return

