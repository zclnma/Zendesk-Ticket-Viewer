import requests
import json
#import getpass
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
        self.auth = self.__base64_auth('%s:%s' % (self.username, self.password))
        self.tickets = self.__retrieve_data(url,self.auth)
        f = open('res.txt', 'w')
        f.write(json.dumps(self.tickets, indent=4, sort_keys=True))

    def __base64_auth(self, auth_str):
        auth = base64.b64encode(auth_str.encode('utf-8')).decode('utf-8')
        return auth

    def __retrieve_data(self, url, auth):
        tickets = []
        s = requests.Session()
        while url:
            for attempt in range(10):
                try:
                    response = s.get(url, headers={'Authorization': 'Basic %s' % auth})
                except requests.exceptions.RequestException as msg:
                    print(msg + '\nReconnecting')
                else:
                    break
            else:
                print('Unable to connect to {url}')
                sys.exit()

            json_data = response.json()
            for ticket in json_data['tickets']:
                tickets.append(ticket)
            url = json_data['next_page']
        return tickets

    #def start_


def main():
    #if len(sys.argv) == 1:
    print('Welcome to the ticket Viewer')
    user_input = input('Type menu to view options or quit to exit\n')
    if(user_input == 'menu'):
        print('ticket1: Hi lionel')
    if(user_input == 'quit'):
        print('Thanks for using ticket Viewer')
        sys.exit()
    #a = Ticket()


if __name__ == '__main__':
    main()
