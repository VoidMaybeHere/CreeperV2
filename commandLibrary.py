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

def incStat(user: discord.User, guild: discord.Guild, stat: str):
    gid = f"{guild.id}"
    uid = f"{user.id}"

    try:
        num = stats[gid][uid][stat]
    except:
        stats[gid] = {uid: {stat: 0}} 
        num = 0
    num += 1
    p.pprint(num)
    stats[gid] = {uid: {stat: num}} 

def getStats(json):
    global stats
    stats = json

def writeJson(logger: logging.Logger):
    logger.info("Writing stats to json file")
    with open("stats.json", "w+") as file:
        file.truncate(0)
        file.write(json.dumps(stats))
        file.close()