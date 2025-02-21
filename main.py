import bot
import argparse

def fail(): raise RuntimeError
    

parser = argparse.ArgumentParser("main.py")
parser.add_argument("-t", help="Token of your discord bot, overrides token set in token.txt", type=str, required=False)
args = parser.parse_args()

if args.t == None:
    try:
        file = open("token.txt", "r")
        token = [line for line in file]
        file.close()
        token = token[0]
        token = token.strip()
    except FileExistsError: fail()
    except FileNotFoundError: fail()

else: 
    token = args.t
    token = token.strip()
        
print(token)

def main(token):
    bot.run(token)

