import requests
import json
import getpass
import sys
import base64

class Ticket:
    def __init__(self,
                 url='https://lionel.zendesk.com/api/v2/tickets.json?per_page=25',
                 username='lionelcdqz@gmail.com',
                 password='zendesk2018'):
        self.url = url
        self.username = username
        self.password = password
        self.auth = self.base64_auth('%s:%s' % (username,password))
        #print (self.auth)

    def base64_auth(self,auth_str):
        auth = base64.b64encode(auth_str.encode('utf-8')).decode('utf-8')
        return auth

def initialize():
    url = 'https://lionel.zendesk.com/api/v2/tickets.json?per_page=25'
    username = 'lionelcdqz@gmail.com'
    password = 'zendesk2018'
    auth_str = '%s:%s' % (username,password)
    tickets = []
    auth = base64.b64encode(auth_str.encode('utf-8')).decode('utf-8')
    while url:
        resdata = requests.get(url, headers={'Authorization': 'Basic %s' % auth}).json()
        print(resdata)
        for ticket in resdata["tickets"]:
            tickets.append(ticket)
            print(tickets[0])
        url = resdata['next_page']
        f = open('res.txt', 'w')
        f.write(json.dumps(resdata["tickets"], indent=4, sort_keys=True))



def main():
    if len(sys.argv) == 1:
        a = Ticket()
if __name__ == '__main__':
    main()
