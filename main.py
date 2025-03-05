import bot
import argparse
import pickle



def fail(error):                                                                                                        #Error ""Handling""
    print(error)    
    raise RuntimeError                                                                                          
    
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
        
def loadStats(file:str="stats.pk1"):
    try:
        with open(file, "rb") as f:
            stats = pickle.load(f)
            f.close()
            return stats
    except FileNotFoundError:
        print("Stats file not found, creating new one")
        with open(file, "wb") as f:
            pickle.dump({}, f)
            f.close()
            return {}
    except Exception as e:
        fail(e)
    

def main(token: str):
    bot.run(token, loadStats())

parser = argparse.ArgumentParser("main.py") 
parser.add_argument("-t", help="Token of your discord bot, overrides token set in token.txt", type=str, required=False) #Token override via -t
args = parser.parse_args()                                                                                              #Parse commandline arguments

if args.t == None:
    token = getTokenFromFile()                                                                                                  #Get token from token.txt
else:                                                                                                                   #Format token string
    token = args.t
    token = token.strip()
    
main(token)                                                                                                             #Run bot with token




