import requests
import json
import sys
import base64
import time
import math


class TicketModel:
    def __init__(self):
        self.tickets = []

    #update ticket in TicketModel from the server
    def __update_tickets(self,tickets):
        self.tickets = tickets

    #retrieve tickets from the server. Use base64 basic Authentication.
    #will attempt 10 times to connect to the server. If failed the system will exit
    #will invoke update_ticket method at last to update ticket in the model once retrive data from the server
    def retrieve_ticket(self, url, auth):
        print('Connecting to ' + url + '...')
        s = requests.Session()
        tickets = []

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
                tickets.append(ticket)
            url = json_data['next_page']

        self.__update_tickets(tickets)
        print('Connecting successfully')

    #return ticked in the model to controller
    def get_tickets(self):
        return self.tickets

class TicketView:
    def __init__(self):
        self.__tickets = []

    #update ticket in the view from controller
    def update_tickets_in_view(self,ticket):
        self.__tickets = ticket

    #message appears when ticket viewer system starts
    def startup_message(self):
        print('Welcome to the ticket viewer.')
        print('You can quit ticket viewer by typing "quit" at anytime.')
        print()
        print('-----------------------------------------------------------------')
        print()
        time.sleep(1)

    #message appears when ticket viewer system exits
    def quit_system_message(self):
        print('Thanks for using ticket viewer.')

    #message appears when go back to previous selection
    def go_back_message(self):
        print()
        print('-----------------------------------------------------------------------------\n')
        print()
        time.sleep(0.5)

    #The first option when entering the app. user can update,view or quit system
    def option1(self):
        return input('Type menu to view options or update to update tickets.\n')

    #The following option when user select menu
    def option2(self):
        print('Please select view mode:')
        print('    1: View all tickets')
        print('    2: View one ticket')
        print('    3: Back to menu')
        return input()

    #The following option when user select "view one ticket"
    def single_ticket_option(self, num_of_tickets):
        print('Please select the ticket number(1 - ' + str(num_of_tickets) + ') you want to view '
                                                                                  'or enter back to go back')
        return input()

    #The following option when user select "view all tickets"
    def detail_or_page_changer_option(self):
        return input('Enter ticket ID for more information or '
                          'p + number to go to select page (eg. p2 to go to page 2).'
                          'Type back to go back to mode selection\n')

    #display the detail of a single ticket
    def view_ticket_detail(self, index_of_ticket):
        print(self.__tickets)
        current_ticket = self.__tickets[index_of_ticket - 1]
        print()
        print('Ticket ID: ' + str(index_of_ticket))
        print('Requester ID: ' + str(current_ticket['requester_id']))
        print('Last Update: ' + current_ticket['updated_at'])
        print('Subject: ' + current_ticket['subject'])
        print('Description: ' + current_ticket['description'])
        print()
        print('---------------------------------------------------------------------------')
        print()
        time.sleep(0.8)

    #display the ticket of all tickets in a specific page.
    #ticket per page is set to 25
    def view_all_tickets_in_current_page(self, current_page, total_page):
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


class TicketController:
    def __init__(self):
        self.__url = 'https://lionel.zendesk.com/api/v2/tickets.json?per_page=25'
        self.__username = 'lionelcdqz@gmail.com'
        self.__password = 'zendesk2018'
        self.__tickets = []
        self.model = TicketModel()
        self.view = TicketView()

    #base64 authenticate a string
    def __base64_auth(self, auth_str):
        auth = base64.b64encode(auth_str.encode('utf-8')).decode('utf-8')
        return auth

    #check if a number is string or not
    def __is_int(self,input_str):
        try:
            input_str = int(input_str)
            return isinstance(input_str, int)
        except:
            return False

    #check if a string is a page changer of not
    #eligibal page changer should start with p followed by number less than total page
    def __is_page_changer(self, input_str, total_page):
        if input_str.startswith('p') and self.__is_int(input_str[1:]):
            if 0 < int(input_str[1:]) <= total_page:
                return True
            else:
                return False
        else:
            return False

    #The whole system starts
    def run(self):

        ##auth string after base64 authentication
        auth = self.__base64_auth('%s:%s' % (self.__username, self.__password))


        ##1. Retrieve tickets from the server
        self.model.retrieve_ticket(self.__url, auth)

        ##2. Get tickets from the model and update tickets in the view
        self.__tickets = self.model.get_tickets()
        self.view.update_tickets_in_view(self.__tickets)

        ##3. Show system startup message
        self.view.startup_message()

        ##4. Start the ticket viewer system
        while True:

            #will check all input from user. If any input is 'quit', the whole system will quit

            #answer 1 can be quit, menu, or update. Will execute different code
            answer1 = self.view.option1()

            if answer1 == 'quit':
                self.view.quit_system_message()
                sys.exit()

            elif answer1 == 'menu':
                #go the the next option once menu is selected

                while True:
                    answer2 = self.view.option2()
                    if answer2 == 'quit':
                        self.view.quit_system_message()
                        sys.exit()

                    elif answer2 == '1':
                        #first page is set to 1 instead of 0.
                        #ticket ID will start with 1 instead of 0.
                        current_page = 1
                        total_page = math.ceil(len(self.__tickets) / 25)

                        #check if the user is going back from ticket detail viewer.
                        #if true, tickets in current page will not be typed again.
                        back_from_detail = False

                        while True:
                            if not back_from_detail:
                                self.view.view_all_tickets_in_current_page(current_page, total_page)

                            #get input from question of viewing ticket detail or changing page
                            detail_or_change_page = self.view.detail_or_page_changer_option()

                            if detail_or_change_page == 'quit':
                                self.view.quit_system_message()
                                sys.exit()

                            elif detail_or_change_page == 'back':
                                self.view.go_back_message()
                                break

                            elif self.__is_int(detail_or_change_page):

                                if (0 < int(detail_or_change_page) <= 25 and current_page != total_page) \
                                    or (int(detail_or_change_page) + (total_page - 1) * 25 - 1 < len(self.__tickets) and current_page == total_page):

                                    self.view.view_ticket_detail(int(detail_or_change_page) + 25 * (current_page - 1))
                                    back_from_detail = True
                                    continue

                                else:
                                    print('Invalid input. Please enter a number.')
                                    time.sleep(0.5)

                            elif self.__is_page_changer(detail_or_change_page, total_page):
                                current_page = int(detail_or_change_page[1:])
                                back_from_detail = False
                                print()
                                continue

                            else:
                                print('Invalid input')
                                continue

                    elif answer2 == '2':
                        while True:

                            #get the number of user about which ticket they want to view.
                            selected_ticket = self.view.single_ticket_option(len(self.__tickets))

                            if selected_ticket == 'quit':
                                self.view.quit_system_message()
                                sys.exit()

                            elif selected_ticket == 'back':
                                self.view.go_back_message()
                                break

                            #check if the input is valid. If so show detail
                            elif self.__is_int(selected_ticket):
                                if 0 < int(selected_ticket) <= len(self.__tickets):
                                    self.view.view_ticket_detail(int(selected_ticket))
                                else:
                                    print('Invalid input. Please enter a number between 1 and ' + str(len(self.__tickets)) + '.')
                                    time.sleep(0.5)
                            else:
                                print('Invalid input. Please enter a quit, back or a number between 1 and ' + str(len(self.__tickets)) + '.')
                                time.sleep(0.5)

                    elif answer2 == '3':
                        self.view.go_back_message()
                        break
                    else:
                        print('Invalid input. Please enter a number between 1 and 3.')

            #Update current tickets if user requires to update
            elif answer1 == 'update':
                self.model.retrieve_ticket(self.__url, auth)
                self.__tickets = self.model.get_tickets()

            else:
                print('Invalid input. Please enter menu or quit')
                time.sleep(0.8)
                continue


def main():
    ticket_system = TicketController()
    ticket_system.run()


if __name__ == '__main__':
    main()
