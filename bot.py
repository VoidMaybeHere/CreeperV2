import discord
import logging
import pprint as p




logger = logging.getLogger('discord') #just copy log handler from discord.py docs
logger.setLevel(logging.DEBUG)
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




class Bot(discord.Client):
    async def on_ready(self):
        p.pprint("Bot Successfully Connected!\n Starting services")
        

        
    






intents = discord.Intents.default()
intents.message_content = True

bot = Bot(intents=intents)

def run(token):
    print("Attempting run")
    bot.run(token=token)