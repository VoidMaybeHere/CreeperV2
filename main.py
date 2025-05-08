from bot import run
import os
from pathlib import Path
from arguments import args #Import commandline arguments namespace as args
from logHandler import logHandler


logger = logHandler.genLogger(logHandler, logName="Main") #Initialize logger

def fail(error):                                                                                                        #Error ""Handling""
    print(error)    
    raise RuntimeError      

def getTokenFromEnv():                                                                                                      #Get token from environment variable
    return os.environ["BOT_TOKEN"]
                                                                                       
    

def runningInDocker():
    if args.d == None:
        return False
    return args.d
    

def main(token: str, logger):
    Path("./data/log").mkdir(parents=True, exist_ok=True)
    run(token, args, logger)   #Run bot with token and runtime args

if args.t == None:
    token = getTokenFromEnv()
                                                                                               #Get token from token.txt
else:                                                                                                                   #Format token string
    token = args.t
    token = token.strip()
    
main(token,logger)                                                                                                             #Run bot with token





