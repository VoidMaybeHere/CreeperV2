import discord
import logging

token = ""

class Bot(discord.Client):
    def on_ready():
        pass




intents = discord.Intents.default()
intents.message_content = True

bot = Bot(intents=intents)
client.run(token)