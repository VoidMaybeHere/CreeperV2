import discord, logging
from StatHandler import StatHandler
import logHandler

class MessageHandler(logHandler.logHandler):
    def __init__(self, statHandler: StatHandler):
        self.StatHandler = statHandler
        self._logger = super().genLogger(self.__name__)
        

        

    def containsTrackedWord(self, message: discord.Message): # Check if a message contains a tracked word
        trackedWords = self.StatHandler.getTrackedWords(message.guild.id)
        if trackedWords == {"Words": {}}:
            return False
        try:
            for key in trackedWords.keys():
                if key in message.content.lower().split():
                    return self._respondToWord(message, trackedWords)
        except KeyError as ke:
            self._logger.debug(f"KeyError: {ke}")
            return False
        return False
    
    def _respondToWord(self, message: discord.Message, trackedWords: dict): # Find a tracked word in a message and return the response if there is one in stats
        messageTextLowerList = message.content.lower().split()
        if trackedWords == {}:
            self._logger.debug(f"Tracked words dict is empty in server {message.guild.id}")
            return ""
        response = ""
        for key in trackedWords.keys(): #for every tracked word in the server
            for word in messageTextLowerList: #For every occurance of a tracked word in the message
                    if word == key:
                        if trackedWords["Words"][key] != "":
                            response += trackedWords["Words"][key] + "\n" #Add response on newline from dict
                        self.StatHandler.incStat(message.author, message.guild, key) #Add 1 to stat counter per word found in message
        return response

    



