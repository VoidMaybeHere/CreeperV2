from bot import run
import argparse
import pickle
import os
from pathlib import Path

defaultFile = "stats.pk1"
dockerPath = "./data/"
Path("./data/log").mkdir(parents=True, exist_ok=True)

def fail(error):                                                                                                        #Error ""Handling""
    print(error)    
    raise RuntimeError      

def getTokenFromEnv():                                                                                                      #Get token from environment variable
    return os.environ["BOT_TOKEN"]
                                                                                       
    

def runningInDocker():
    if args.d == None:
        return False
    return args.d
    

def main(token: str):
    run(token, loadStats(runningInDocker()), runningInDocker())                                                                 #Run bot with token and stats

parser = argparse.ArgumentParser("main.py") 
parser.add_argument("-d", help="Set true if running in a docker container", type=bool, required=False)
parser.add_argument("-t", help="Token of your discord bot, overrides token set in token.txt", type=str, required=False) #Token override via -t
args = parser.parse_args()                                                                                              #Parse commandline arguments

if args.t == None:
    try:
        token = getTokenFromEnv()
    except Exception as e:
        token = getTokenFromFile()                                                                                                  #Get token from token.txt
else:                                                                                                                   #Format token string
    token = args.t
    token = token.strip()
    
main(token)                                                                                                             #Run bot with token




