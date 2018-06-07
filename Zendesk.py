import requests
import json
import getpass
import sys
import getopt
import math


def initialize(username, password):
    res = requests.get('https://lionel.zendesk.com/api/v2/tickets.json', auth=(username,password))
    resdata = res.json()
    print(resdata)
    print(resdata["tickets"])
    print(json.dumps(resdata["tickets"],indent=4,sort_keys=True))
    f = open('res.txt','w')
    f.write(json.dumps(resdata["tickets"],indent=4,sort_keys=True))

"""def main():
    # parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
        filename = input('Enter a file name\n')
        print(filename)
    except getopt.error as msg:
        print (msg)
        print ("for help use --help")
        sys.exit(2)
    # process options
    for o, a in opts:
        if o in ("-h", "--help"):
            print ("This is help file")
            sys.exit(0)
    # process arguments
    for arg in args:
        print('dsfjksjdhf')  # process() is defined elsewhere"""
def main():
    username = input('Please enter your username\n')
    password = getpass.getpass('Please enter your password\n')
    initialize(username,password)

if __name__ == '__main__':
    main()
