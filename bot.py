import discord, discord.ext
import discord.ext.commands, commandLibrary as c
#logging
import logging, logging.handlers
#CTRL + C Handling
import signal, sys








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




intents = discord.Intents.all() ##FIXME: get regular intents working


bot = discord.ext.commands.Bot(intents=intents, command_prefix='?')




@bot.event    
async def on_ready():
    logger.info("Bot is Ready! Starting Services.")
    await bot.tree.sync()
    logger.info("Command Tree Synced")
    


@bot.listen('on_message')
async def messageHandler(message: discord.Message):
    
    if message.author == bot.user or message.author.bot == True: #check if message was sent by a bot or self
        return None
    print(message.content)
    if message.content.lower() == "creeper":
        c.incStat(message.author, message.guild, "creeper")
        await message.reply("aw man")






#Command Handler
@bot.tree.command(name="test")
@discord.app_commands.describe(arg1 = "Fuck you", arg2 = "Fuck you more")
async def test(interact: discord.Interaction, arg1: int, arg2: str):
    await interact.response.send_message(f"Test command, if you see this <@341767947309678603> fucked up. {arg1} : {arg2}")
    logger.debug(f"Test command fired by {interact.user.name}")

@bot.tree.command(name="stats")
@discord.app_commands.describe(user = "Discord user", word = "Tracked word")
async def getStats(ctx : discord.Interaction, user: discord.User, word: str):
    word = word.lower()
    await ctx.response.send_message(f"{user.mention} has said {word} {c.getStat(ctx.guild, user, word)} times.", ephemeral=True)







def run(token, json):
    logger.info("Attempting to start bot...")
    c.getStats(json)
    bot.run(token=token, reconnect=True)




def stop(sig = None, frame = None):
    
    logger.critical("Stopping Gracefully")
    c.writeJson(logger)
    logger.warning("Exiting Program")
    sys.exit(0)

signal.signal(signal.SIGINT, stop) #CTRL + C Handler