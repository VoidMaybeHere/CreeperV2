import argparse


parser = argparse.ArgumentParser("main.py") 
parser.add_argument("-d", help="Set true if running in a docker container", type=bool, required=False)
parser.add_argument("-t", help="Token of your discord bot, overrides token set in token.txt", type=str, required=False) #Token override via -t
args = parser.parse_args() #Parse commandline arguments