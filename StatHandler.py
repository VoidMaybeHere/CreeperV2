from FileHandler import pkFileHandler as FileHandler
import logging
import discord

class StatHandler:
    def __init__(self, docker:bool = False):
        
        
        
        
        
        self._generateLogger()
        
        self._fileHandler = FileHandler(docker=docker)
        self.stats = self._fileHandler.load()
        
    def getServerStats(self, guild: discord.Guild):# Get combined stats for all users in a server
        guild = f"{guild.id}"
        serverStatsString = ""
        try:
            for user in self.stats[guild].keys():
                if user != "Words":
                    userStatsString = f"<@{user}>:\n"
                    try:
                        for key in self.stats[guild][user].keys():
                            userStatsString += f"{key}: {self.stats[guild][user][key]}\n"
                        serverStatsString += userStatsString
                    except:
                        serverStatsString += f"<@{user}>: No stats found\n"
        except KeyError as ke:
            self._logger.info(f"KeyError: {ke}")
            serverStatsString = "No Stats Recorded in Server."
        except Exception as e:
            self._logger.error(f"Error getting server stats: {e}")
            serverStatsString = "Error getting server stats"

        if serverStatsString == "" or serverStatsString == None:
            self._logger.error(f"Server stats string is empty, \"{serverStatsString}\"")
            serverStatsString = "No stats recorded in server and bot really fucked up"
        return serverStatsString    
    
    def getAllStats(self, guild: discord.Guild, user: discord.User): # Get all stats for a user in a server
        guild = f"{guild.id}"
        user = f"{user.id}"
        userStatsString = ""
        try:
            userStats = self.stats[guild][user]
            for key in userStats.keys():
                userStatsString += f"{key}: {userStats[key]}\n"
        except Exception as e:
            self._logger.error(f"Error getting all stats: {e}")
            userStatsString = "No stats found"
        return userStatsString
        
    def getStat(self, guild: discord.Guild, user: discord.User, word: str): # Get a specific stat for a user in a server
        guild = f"{guild.id}"
        user = f"{user.id}"
        try:
            stat = self.stats[guild][user][word]
        except Exception as e:
            self._logger.debug(f"Unable to get stat for {user} due to : {e}") 
            stat = 0
        return stat
        
    def incStat(self, user: discord.User, guild: discord.Guild, word: str): # Increase a specific stat by 1 and create it in a users stats if it does not exist
        gid = f"{guild.id}"
        uid = f"{user.id}"
        try:
            self.stats[gid][uid]
        except KeyError:
            try:
                self.stats[gid][uid] = {}
                self._logger.info(f"KeyError: {uid} not found in stats, creating empty dict")
            except KeyError:
                self.stats[gid] = {uid: {}}
                self._logger.info(f"KeyError: {gid} not found in stats, creating empty dict")
            
        try:
            num = self.stats[gid][uid][word]
        except Exception as e:
            self._logger.info(f"Error getting stat: {word} due to {e} {e.__class__}")
            self._logger.info(self.stats)

            self.stats[gid][uid][word] = 0
            self._logger.info(self.stats) 
            num = 0
        num += 1
        self.stats[gid][uid][word] = num

    
    
    def getTrackedWords(self, gid: int): # Get the words from the "Words" entry from stats[GuildID]
        gid = f"{gid}"
        try:
            return self.stats[f"{gid}"]["Words"]
        except KeyError:
            self._logger.debug(f"KeyError: Words dict not found in gid {gid}")
            self.stats[gid] = {"Words": {}}
            return {"Words": {}}
        except Exception as e:
            self._logger.debug(f"Error getting tracked words: {e}")
            return {"Words": {}}
        
    
        
    def _generateLogger(self):
        Log = logging.getLogger("Stat Handler")
        Log.addHandler(logging.StreamHandler())
        Log.addHandler(logging.FileHandler(filename=self.__name__+".log", mode="a", encoding="utf-8").setFormatter(formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')))
        Log.setLevel(logging.INFO)
        Log.info("Logger Initalized")
        self._logger = Log