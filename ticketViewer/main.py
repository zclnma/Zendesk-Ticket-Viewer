import requests
import json
import sys
import base64
import time
import math


class Ticket(object):
    def __init__(self,url, username, password):
        self.__url = url
        self.__username = username
        self.__password = password
        self.__auth = self.__base64_auth('%s:%s' % (self.__username, self.__password))
        self.__tickets = self.__retrieve_data(self.__url,self.__auth)
        f = open('res.txt', 'w')
        f.write(json.dumps(self.__tickets, indent=4, sort_keys=True))

    def __base64_auth(self, auth_str):
        auth = base64.b64encode(auth_str.encode('utf-8')).decode('utf-8')
        return auth

    def __is_int(self,input_str):
        try:
            input_str = int(input_str)
            return isinstance(input_str, int)
        except:
            return False

    def __is_page_changer(self, input_str, total_page):
        if input_str.startswith('p') and self.__is_int(input_str[1:]):
            if 0 < int(input_str[1:]) <= total_page:
                return True
            else:
                return False
        else:
            return False


    def __retrieve_data(self, url, auth):
        json_tickets = []
        s = requests.Session()
        while url:
            for attempt in range(10):
                try:
                    response = s.get(url, headers={'Authorization': 'Basic %s' % auth})
                except requests.exceptions.RequestException as msg:
                    print(msg)
                    time.sleep(0.3)
                    print('Reconnecting...')
                else:
                    break
            else:
                print('Unable to connect to ' + url)
                sys.exit()

            json_data = response.json()
            for ticket in json_data['tickets']:
                json_tickets.append(ticket)
            url = json_data['next_page']

        return json_tickets

    def get_tickets(self):
        return self.__tickets

    def view_all_tickets(self):
        current_page = 1
        total_page = math.ceil(len(self.__tickets) / 25)
        while True:
            for instance in range(25):
                ID = instance + 25 * (current_page - 1)
                if current_page != total_page:
                    current_ticket = self.__tickets[ID]
                elif current_page == total_page and ID < len(self.__tickets):
                    current_ticket = self.__tickets[ID]
                else:
                    break

                print('Ticket ID: ' + str(instance + 1) +
                      ' Requester: ' + str(current_ticket['requester_id']) +
                      ' Subject: ' + current_ticket['subject'])

            print()
            print('-----------------------------------------------------------------------------\n')
            print()
            print('Page: ' + str(current_page) + '/' + str(total_page))
            print()
            selection = input('Enter ticket ID for more information or '
                               'p + number to go to select page (eg. p2 to go to page 2).'
                               'Type back to go back to mode selection\n')
            if selection == 'quit':
                print('Thanks for using ticket viewer.')
                sys.exit()
            elif selection == 'back':
                print()
                print('-----------------------------------------------------------------------------\n')
                print()
                time.sleep(0.5)
                break
            elif self.__is_int(selection):

                if (0 < int(selection)<= 25 and current_page != total_page) or (int(selection) + (total_page - 1) * 25 - 1<= len(self.__tickets) and current_page == total_page):
                    self.view_ticket_detail(int(selection) + 25 * (current_page - 1))
                    continue
                else:
                    print('Invalid input. Please enter a number.')

            elif self.__is_page_changer(selection,total_page):
                current_page = int(selection[1:])
                print()
                continue

            else:
                print('Invalid input')
                continue

    def view_single_ticket(self):
        while True:
            print('Please select the ticket number(1 - ' + str(len(self.__tickets)) + ') you want to view '
                'or input back to go back')

            selected_ticket = input()
            if selected_ticket == 'quit':
                print('Thanks for using ticket viewer.')
                sys.exit()
            elif selected_ticket == 'back':
                print()
                print('-----------------------------------------------------------------------------\n')
                print()
                time.sleep(0.5)
                break

            elif self.__is_int(selected_ticket):
                if 0 < int(selected_ticket) <= len(self.__tickets):
                    self.view_ticket_detail(int(selected_ticket))
                else:
                    print('Invalid input. Please enter a number between 1 and ' + str(len(self.__tickets)) + '.')
                    time.sleep(0.5)
            else:
                print('Invalid input. Please enter a number.')
                time.sleep(0.5)

    def view_ticket_detail(self,ticket_num):
        current_ticket = self.__tickets[ticket_num - 1]
        print()
        print('Ticket ID: ' + str(ticket_num))
        print('Requester ID: ' + str(current_ticket['requester_id']))
        print('Last Update: ' + current_ticket['updated_at'])
        print('Subject: ' + current_ticket['subject'])
        print('Description: ' + current_ticket['description'])
        print()
        print('---------------------------------------------------------------------------')
        print()
        time.sleep(0.5)

    def update_tickets(self):
        print('Updating tickets...')
        self.__tickets = self.__retrieve_data(self.__url, self.__auth)
        print('Successfully updating tickets.')
        print()
        print('-----------------------------------------------------------------------------\n')
        print()
        time.sleep(0.5)

def viewer_system(ticket_viewer):
    print('Welcome to the ticket viewer.')
    print('You can quit ticket viewer by typing "quit" at anytime.')
    print()
    print('-----------------------------------------------------------------')
    print()
    time.sleep(1)
    while True:
        user_input = input('Type menu to view options or update to update tickets.\n')
        if user_input == 'quit':
            print('Thanks for using ticket viewer.')
            sys.exit()
        else:
            if user_input == 'menu':
                while True:
                    print('Please select view mode:')
                    print('    1: View all tickets')
                    print('    2: View one ticket')
                    print('    3: Back to menu')
                    mode = input()
                    if mode == 'quit':
                        print('Thanks for using ticket viewer.')
                        sys.exit()
                    elif mode == '1':
                        ticket_viewer.view_all_tickets()
                    elif mode == '2':
                        ticket_viewer.view_single_ticket()
                    elif mode == '3':
                        print()
                        print('-----------------------------------------------------------------------------\n')
                        print()
                        time.sleep(0.5)
                        break
                    else:
                        print('Invalid input. Please enter a number between 1 and 3.')

            elif user_input == 'update':
                ticket_viewer.update_tickets()

            else:
                print('Invalid input.')
                time.sleep(0.5)
                continue

def main():
    url = 'https://lionel.zendesk.com/api/v2/tickets.json?per_page=25'
    username = 'lionelcdqz@gmail.com'
    password = 'zendesk2018'
    print('Connecting to ' + url + '...')
    ticket_viewer = Ticket(url, username, password)
    print('Connecting successfully')
    time.sleep(1)

    viewer_system(ticket_viewer)


if __name__ == '__main__':
    main()
