import discord
import logging, logging.handlers
import pprint as p




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




intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)





@bot.event    
async def on_ready():
    logger.info("Bot is Ready! Starting Services.")
    


'''@bot.listen('on_message')
async def messageHandler(message):
    pass'''

    #Command Handler
    
        

        
    








def run(token):
    logger.info("Attempting to start bot...")
    bot.run(token=token)