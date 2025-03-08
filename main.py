from bot import run
import argparse
import pickle
import os
from pathlib import Path

defaultFile = "stats.pk1"
dockerPath = "./data/"

def fail(error):                                                                                                        #Error ""Handling""
    print(error)    
    raise RuntimeError      

def getTokenFromEnv():                                                                                                      #Get token from environment variable
    return os.environ["BOT_TOKEN"]
                                                                                       
    
def getTokenFromFile():                                                                                                         #Get token from token.txt
    try:
        file = open("token.txt", "r") 
        token = [line for line in file]                                                                                 #Get all lines in file
        file.close()
        token = token[0]
        token = token.strip()
        return token
    except FileExistsError: 
        open("token.txt", "x").close()
        print("Token file created, please put your token in token.txt")
        fail(FileExistsError)
    except Exception as e:
        fail(e)
        
def loadStats(runningInDocker: bool):                                                                                                  #Load stats from file
    if runningInDocker:
        file = dockerPath + defaultFile
        Path(dockerPath).mkdir(parents=True, exist_ok=True)
    else:
        file = defaultFile
    print(f"Loading stats from {file}")
    try:
        with open(file, "rb") as f:
            stats = pickle.load(f)
            f.close()
            print(stats)
            return stats
    except FileNotFoundError:
        print("Stats file not found, creating new one")
        with open(file, "wb") as f:
            pickle.dump({}, f)
            f.close()
            return {}
    except Exception as e:
        fail(e)

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




