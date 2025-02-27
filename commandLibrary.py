import discord, pprint as p, logging, pickle


stats = {}

def getStat(guild: discord.Guild, user: discord.User, word: str):
    guild = f"{guild.id}"
    user = f"{user.id}"
    try:
        stat = stats[guild][user][word]
    except: 
        stat = 0
    return stat

def incStat(user: discord.User, guild: discord.Guild, word: str):
    gid = f"{guild.id}"
    uid = f"{user.id}"

    try:
        num = stats[gid][uid][word]
    except:
        stats[gid] = {uid: {word: 0}} 
        num = 0
    num += 1
    p.pprint(num)
    stats[gid] = {uid: {word: num}} 

def getStats(pk1):
    global stats
    stats = pk1

def saveStats(logger: logging.Logger):
    logger.info("Writing stats to pickle file")
    with open("stats.pk1", "wb") as f:
        pickle.dump(stats, f)
        f.close()
    logger.info("Stats written to pickle file")
        
def bypass(user: discord.Member, logger: logging.Logger):
    rString = "Error bypassing "
    error = False
    try:
        if user.voice.mute:
            user = user.edit(mute=False)
    except Exception as e:
        error = True
        logger.error(f"Error bypassing mute: {e}")
        rString += "mute"
    try:
        if user.voice.deaf:
            user.edit(deafen=False)
            
    except Exception as e:
        error = True
        logger.error(f"Error bypassing deafen: {e}")
        if rString.endswith("mute"):
            rString += "/deafen"
    if error:
        return rString
    return "Success"

def trackWord(ctx: discord.Interaction, word: str, response: str, logger: logging.Logger):
    gid = ctx.guild.id
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
        
def respondToWord(message: discord.Message):
    response = ""
    for key in stats[f"{message.guild.id}"]["Words"]: #for every tracked word in the server
        for key in message.content.lower(): #For every occurance of a tracked word in the message
            if stats[f"{message.guild.id}"]["Words"][key] != "":
                response += stats[f"{message.guild.id}"]["Words"][key] + "\n" #Add response on newline from dict
            incStat(message.author, message.guild, key) #Add 1 to stat counter per word found in message
    return response
    
def isTrackedWord(message: discord.Message):
    try:
        if any(message.content.lower().split()) in stats[f"{message.guild.id}"]["Words"].keys():
            return True
    except KeyError as ke:
        print(f"KeyError: {ke}")
        return False
    
                
        
    
    
        