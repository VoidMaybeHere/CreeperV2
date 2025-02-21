import discord
import logging
import pprint as p


class Bot(discord.Client):
    async def on_ready(self):
        p.pprint("Bot Successfully Connected!\n Starting services")

        
    






intents = discord.Intents.default()
intents.message_content = True

bot = Bot(intents=intents)

def run(token):
    print("Attempting run")
    bot.run(token=token)