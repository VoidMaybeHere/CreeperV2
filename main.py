import bot
import argparse
import os
import json



def fail(error):                                                                                                        #Error ""Handling""
    print(error)    
    raise RuntimeError                                                                                          
    

parser = argparse.ArgumentParser("main.py") 
parser.add_argument("-t", help="Token of your discord bot, overrides token set in token.txt", type=str, required=False) #Token override via -t
args = parser.parse_args()                                                                                              #Parse commandline arguments

if args.t == None:
    try:
        file = open("token.txt", "r") 
        token = [line for line in file]                                                                                 #Get all lines in file
        file.close()
        token = token[0]
        token = token.strip()
    except FileExistsError: 
        open("token.txt", "x").close()
        print("Token file created, please put your token in token.txt")
        fail(FileExistsError)
    except Exception as e:
        fail(e)

else:                                                                                                                   #Format token string
    token = args.t
    token = token.strip()









def loadStats(statsFile):
    stat = json.load(statsFile)
    statsfile.close()
    return stat

def main(token: str, stats: dict):
    bot.run(token, stats)






if not os.path.exists("stats.json"):
    statsfile = open("stats.json", "x")
    statsfile.close()
    main(token, {})
else:
    statsfile = open("stats.json", "r")
    main(token, loadStats(statsfile))


