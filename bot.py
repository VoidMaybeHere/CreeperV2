import discord
import logging


class Bot(discord.Client):
    def on_ready():
        pass





intents = discord.Intents.default()
intents.message_content = True

bot = Bot(intents=intents)

def run(token):
    bot.run(token)