import discord, discord.ext
import logging, logging.handlers
import pprint as p

import discord.ext.commands




logger = logging.getLogger('discord') #just copy log handler from discord.py docs
logger.setLevel(logging.DEBUG)
logging.getLogger('discord.http').setLevel(logging.DEBUG)

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
    p.pprint(message.content.lower())
    if message.content.lower() == "creeper":
        await message.reply("aw man")

    #Command Handler

@bot.tree.command(name="test")
@discord.app_commands.describe(arg1 = "Fuck you", arg2 = "Fuck you more")
async def test(interact: discord.Interaction, arg1: int, arg2: str):
    await interact.response.send_message(f"Test command, if you see this <@341767947309678603> fucked up. {arg1} : {arg2}")
    logger.debug(f"Test command fired by {interact.user.name}")


        
    








def run(token):
    logger.info("Attempting to start bot...")
    bot.run(token=token)