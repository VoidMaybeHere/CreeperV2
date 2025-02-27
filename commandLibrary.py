import discord, pprint as p, logging, json


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

def getStats(json):
    global stats
    stats = json

def writeJson(logger: logging.Logger):
    logger.info("Writing stats to json file")
    with open("stats.json", "w+") as file:
        file.truncate(0)
        file.write(json.dumps(stats))
        file.close()
        
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
    
    try:
        stats[gid]["Words"][word] = response
    except KeyError:
        stats[gid] = {"Words": {word: response}}
    except Exception as e:
        logger.error(f"Error tracking word: {e}")
        
def respondToWord(message: discord.Message):
    response = ""
    for key in stats[f"{message.guild.id}"]["Words"]:
        for key in message.content.lower():
            response += stats[f"{message.guild.id}"]["Words"][key] + "\n"
    return response
    
def isTrackedWord(message: discord.Message):
    if message.content.lower() in stats[f"{message.guild.id}"]["Words"]:
        return True
    return False
                
        
    
    
        