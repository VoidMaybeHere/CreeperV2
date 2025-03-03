import discord, pprint as p, logging, pickle


stats = {}
logger = None

def getStat(guild: discord.Guild, user: discord.User, word: str):
    guild = f"{guild.id}"
    user = f"{user.id}"
    try:
        stat = stats[guild][user][word]
    except: 
        stat = 0
    return stat

def getAllStats(guild: discord.Guild, user: discord.User):
    guild = f"{guild.id}"
    user = f"{user.id}"
    userStatsString = ""
    try:
        userStats = stats[guild][user]
        for key in userStats.keys():
            userStatsString += f"{key}: {userStats[key]}\n"
    except Exception as e:
        logger.error(f"Error getting all stats: {e}")
        userStatsString = "No stats found"
    return userStatsString

def incStat(user: discord.User, guild: discord.Guild, word: str):
    gid = f"{guild.id}"
    uid = f"{user.id}"
    try:
        stats[gid][uid]
    except KeyError:
        stats[gid][uid] = {}
        logger.info(f"KeyError: {uid} not found in stats, creating empty dict")
    try:
        num = stats[gid][uid][word]
    except Exception as e:
        logger.info(f"Error getting stat: {word} due to {e} {e.__class__}")
        logger.info(stats)

        stats[gid][uid][word] = 0
        logger.info(stats) 
        num = 0
    num += 1
    stats[gid][uid][word] = num

def loadStats(pk1):
    global stats
    stats = pk1

def getLogger(tlogger: logging.Logger):
    global logger
    logger = tlogger

def saveStats():
    logger.info("Writing stats to pickle file")
    with open("stats.pk1", "wb") as f:
        pickle.dump(stats, f)
        f.close()
    logger.info("Stats written to pickle file")
        
async def bypass(user: discord.Member):
    rString = "Error bypassing "
    error = False
    try:
        if user.voice.mute:
            user = await user.edit(mute=False)
    except Exception as e:
        error = True
        logger.error(f"Error bypassing mute: {e}")
        rString += "mute"
    try:
        if user.voice.deaf:
           await user.edit(deafen=False)
            
    except Exception as e:
        error = True
        logger.error(f"Error bypassing deafen: {e}")
        if rString.endswith("mute"):
            rString += "/deafen"
    if error:
        return rString
    return "Success"

def trackWord(ctx: discord.Interaction, word: str, response: str):
    gid = f"{ctx.guild.id}"
    word = word.lower()
    if response == None:
        response = ""
    
    try:
        stats[gid]["Words"][word] = response
    except KeyError:
        stats[gid] = {"Words": {word: response}}
    except Exception as e:
        logger.error(f"Error tracking word: {e}")
        return f"Error tracking word: {e}"
    
    logger.info(f"Word [{word}] with response [{response}] added to tracked words dict in server {gid}")
    return f"Word [{word}] with response [{response}] added to tracked words dict in server {gid}"

def untrackWord(ctx: discord.Interaction, word: str):
    gid = f"{ctx.guild.id}"
    word = word.lower()
    try:

        for user in stats[gid].keys():
            if user != "Words":
                for trackedWord in stats[gid][user].keys():
                    if trackedWord == word:
                        del stats[gid][user][word]
                        break
                    

        del stats[gid]["Words"][word]
    except KeyError as ke:
        logger.info(f"KeyError: {word} not found in tracked words dict in server {gid}... {ke}")
        return f"Word [{word}] not found in tracked words dict in server {gid}"
    except Exception as e:
        logger.error(f"Error untracking word: {e}")
        return f"Error untracking word: {e}"
    
    logger.info(f"Word [{word}] removed from tracked words dict in server {gid}")
    return f"Word [{word}] removed from tracked words dict in server {gid}"
        
def respondToWord(message: discord.Message):
    trackedWords = getTrackedWords(message.guild.id)
    messageTextLowerList = message.content.lower().split()
    if trackedWords == {}:
        logger.debug(f"Tracked words dict is empty in server {message.guild.id}")
        return ""
    response = ""
    for key in trackedWords.keys(): #for every tracked word in the server
        for word in messageTextLowerList: #For every occurance of a tracked word in the message
            

                if word == key:
                    if stats[f"{message.guild.id}"]["Words"][key] != "":
                        response += stats[f"{message.guild.id}"]["Words"][key] + "\n" #Add response on newline from dict
                    incStat(message.author, message.guild, key) #Add 1 to stat counter per word found in message
            

    return response

def getTrackedWords(gid: int):
    gid = f"{gid}"
    try:
        return stats[f"{gid}"]["Words"]
    except KeyError:
        logger.debug(f"KeyError: Words dict not found in gid {gid}")
        stats[gid] = {"Words": {}}
        return {}
    except Exception as e:
        logger.debug(f"Error getting tracked words: {e}")
        return {}
    
def isTrackedWord(message: discord.Message):
    trackedWords = getTrackedWords(message.guild.id)
    if trackedWords == {}:
        return False
    try:
        for key in trackedWords.keys():
            if key in message.content.lower().split():
                return True
    except KeyError as ke:
        logger.debug(f"KeyError: {ke}")
        return False
    return False
    
                
        
    
    
        