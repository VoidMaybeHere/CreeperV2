import discord, discord.ext
import discord.ext.commands, commandLibrary as c
#logging
import logging, logging.handlers
#CTRL + C Handling
import signal, sys, os








logger = logging.getLogger('discord') #just copy log handler from discord.py docs
logger.setLevel(logging.INFO)
logging.getLogger('discord.http').setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(
    filename='discord.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=5,  # Rotate through 5 files
)
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info("Logger setup")
c.getLogger(logger) #get logger into commandLibrary




intents = discord.Intents.none() 
intents.message_content = True
intents.voice_states = True
intents.dm_reactions = True
intents.dm_messages = True
intents.guild_messages = True
intents.guilds = True


bot = discord.ext.commands.Bot(intents=intents, command_prefix='?')




@bot.event    
async def on_ready():
    logger.info("Current pid: " + str(os.getpid()))
    await bot.tree.sync()
    logger.info("Command Tree Synced")
    logger.info("Bot is Ready! Starting Services.")
    await bot.change_presence(activity=discord.CustomActivity(name="aw man"))
    
    


@bot.listen('on_message')
async def messageHandler(message: discord.Message):
    
    if message.author == bot.user or message.author.bot == True: #check if message was sent by a bot or self
        return None
    
    
    if "creeper" in message.content.lower():
        reply = ""
        for word in message.content.lower().split():
            if word == "creeper":
                reply += "aw man\n"
        c.incStat(message.author, message.guild, "creeper")
        await message.reply(reply)
        return
        
    if message.content.lower() == "by the will of allah i shall surpass the mute" or message.content.lower() == "by the will of allah i shall surpass the deafen":
        if message.author.id == 341767947309678603: #my id
            await message.author.send(await c.bypass(message))
            return
            
    if c.isTrackedWord(message):
        response = c.respondToWord(message)
        if response != "" and response != None:
            await message.reply(response)
        return






#Command Handler

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
    
@bot.tree.command(name="track", description="Track a word and give a response")
@discord.ext.commands.has_permissions(manage_guild=True)
@discord.app_commands.describe(word = "Word to track", response = "Response to give, if any")
async def addWord(ctx: discord.Interaction, word: str, response: str=None): # Adds a word to the tracked words dict
    await ctx.response.send_message(c.trackWord(ctx,word,response), ephemeral=True)

@bot.tree.command(name="untrack", description="Untrack a word, if it exists")
@discord.ext.commands.has_permissions(manage_guild=True)
@discord.app_commands.describe(word = "Word to untrack")
async def removeWord(ctx: discord.Interaction, word: str): # Removes a word from the tracked words dict
    await ctx.response.send_message(c.untrackWord(ctx,word), ephemeral=True)






def run(token, pk1, docker: bool=False):

    handler.doRollover()
    logger.info("Attempting to start bot...")
    c.docker = docker
    c.inDocker(docker)
    c.loadStats(pk1)
    bot.run(token=token, reconnect=True)




def stop(sig = None, frame = None):
    
    logger.warning("Stopping Gracefully")
    c.saveStats()
    logger.critical("Exiting Program")
    sys.exit(0)

signal.signal(signal.SIGINT, stop) #CTRL + C Handler
signal.signal(signal.SIGTERM, stop) #SIGTERM Handler