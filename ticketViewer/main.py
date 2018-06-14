"""This module can retrieve tickets from Zendesk website with username&password access
    and allow users to view those tickets in CLI
        14/06/2018 -- Lionel
"""

import sys
import base64
import time
import math
import configparser

import requests


class TicketModel:
    """Class for retrieve, update and store tickets."""

    def __init__(self):
        """__init__ function defines tickets list"""
        self.__tickets = []

    def __update_tickets(self, tickets):
        """update ticket in TicketModel from the server"""
        self.__tickets = tickets

    def retrieve_ticket(self, url, auth):
        """retrieve tickets from the server. Use base64 basic Authentication.
        will attempt 2 times to connect to the server. If failed the system will exit
        will invoke update_ticket method at last to update ticket in the
        model once retrive data from the server"""

        print('Connecting to ' + url + '...')
        ticket_session = requests.Session()
        tickets = []

        while url:
            for _ in range(2):
                try:
                    response = ticket_session.get(url, headers={'Authorization': 'Basic %s' % auth})
                except requests.exceptions.RequestException as msg:
                    print(msg)
                    time.sleep(0.3)
                    print('Reconnecting...')
                else:
                    break
            else:
                print('Unable to connect to ' + url +
                      '. The API is currently not available, please try later ')
                sys.exit()

            json_data = response.json()
            tickets.extend(json_data['tickets'])
            url = json_data['next_page']

        ticket_session.close()
        self.__update_tickets(tickets)
        print('Connecting successfully')

    def get_tickets(self):
        """return ticked in the model to controller"""
        return self.__tickets


class TicketView:
    """class for display most message in CLI"""

    def __init__(self):
        """store tickets from controller"""
        self.__tickets = []

    def update_tickets_in_view(self, ticket):
        """update ticket in the view from controller"""
        self.__tickets = ticket

    @classmethod
    def startup_message(cls):
        """message appears when ticket viewer system starts"""
        print('Welcome to the ticket viewer.')
        print('You can quit ticket viewer by typing "quit" at anytime.')
        print()
        print('-----------------------------------------------------------------')
        print()
        time.sleep(1)

    @classmethod
    def quit_system_message(cls):
        """message appears when ticket viewer system exits"""
        print('Thanks for using ticket viewer.')

    @classmethod
    def go_back_message(cls):
        """message appears when go back to previous selection"""
        print()
        print('-----------------------------------------------------------------------------\n')
        print()
        time.sleep(0.5)

    @classmethod
    def option1(cls):
        """The first option when entering the app. user can update,view or quit system"""
        return input('Enter menu to view options or update to update tickets.\n')

    @classmethod
    def option2(cls):
        """The following option when user select menu"""
        print('Please select view mode:')
        print('    1: View all tickets')
        print('    2: View one ticket')
        print('    3: Back to menu')
        return input()

    @classmethod
    def single_ticket_option(cls, num_of_tickets):
        """The following option when user select view one ticket."""
        print('Please select the ticket number(1 - ' + str(num_of_tickets) +
              ') you want to view or enter back to go back')
        return input()

    @classmethod
    def detail_or_page_changer_option(cls):
        """The following option when user select view all tickets"""
        return input('Enter ticket ID for more information or '
                     'p + number to go to select page (eg. p2 to go to page 2).'
                     'Enter back to go back to mode selection\n')

    def view_ticket_detail(self, index_of_ticket):
        """display the detail of a single ticket"""
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

    def view_tickets_current_page(self, current_page, total_page, item_per_page):
        """display the ticket of all tickets in a specific page.
        ticket per page is set to 25"""

        for instance in range(item_per_page):
            current_id = instance + item_per_page * (current_page - 1)
            if current_page != total_page:
                current_ticket = self.__tickets[current_id]
            elif current_page == total_page and current_id < len(self.__tickets):
                current_ticket = self.__tickets[current_id]
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
    """Main system running"""

    def __init__(self):
        """
            Read default settings in the config file and instantiate
            view and model class.
        """
        try:
            config = configparser.RawConfigParser()
            config.read('config.txt')
            self.__url = config.get('configuration', 'url')
            self.__username = config.get('configuration', 'username')
            self.__password = config.get('configuration', 'password')
            self.__item_per_page = int(config.get('configuration', 'item_per_page'))
            self.__tickets = []
        except:
            print('Unable to read configuration file.')
            time.sleep(0.5)
            print('Exiting...')
            time.sleep(0.5)
            sys.exit()
        self.model = TicketModel()
        self.view = TicketView()

    @classmethod
    def __base64_auth(cls, auth_str):
        """base64 authenticate a string"""
        auth = base64.b64encode(auth_str.encode('utf-8')).decode('utf-8')
        return auth

    @classmethod
    def __is_int(cls, input_str):
        """check if a number is string or not"""
        try:
            input_str = int(input_str)
            return isinstance(input_str, int)
        except:
            return False

    def __is_page_changer(self, input_str, total_page):
        """"check if a string is a page changer of not
        eligible page changer should start with p followed by number less than total page"""

        if input_str.startswith('p') and self.__is_int(input_str[1:]):
            if 0 < int(input_str[1:]) <= total_page:
                return True
            return False
        return False

    def run(self):
        """System starts"""

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
                        total_page = math.ceil(len(self.__tickets) / self.__item_per_page)

                        #check if the user is going back from ticket detail viewer.
                        #if true, tickets in current page will not be typed again.
                        back_from_detail = False

                        while True:
                            if not back_from_detail:
                                self.view.view_tickets_current_page(
                                    current_page, total_page, self.__item_per_page
                                )

                            #get input from question of viewing ticket detail or changing page
                            detail_or_change_page = self.view.detail_or_page_changer_option()

                            if detail_or_change_page == 'quit':
                                self.view.quit_system_message()
                                sys.exit()

                            elif detail_or_change_page == 'back':
                                self.view.go_back_message()
                                break

                            elif self.__is_int(detail_or_change_page):
                                #check if input is valid
                                if ((0 < int(detail_or_change_page) <= self.__item_per_page)
                                        and (current_page != total_page)) \
                                        or ((int(detail_or_change_page) + (total_page - 1) * self.__item_per_page - 1
                                             < len(self.__tickets))
                                            and(current_page == total_page)):

                                    self.view.view_ticket_detail(
                                        int(detail_or_change_page) + self.__item_per_page * (current_page - 1)
                                    )
                                    back_from_detail = True
                                    continue

                                else:
                                    print('Invalid input. Please enter a valid number')
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
                                    print('Invalid input. Please enter a number between 1 and '
                                          + str(len(self.__tickets)) + '.')
                                    time.sleep(0.5)
                            else:
                                print('Invalid input. Please enter a quit, back or a number between 1 and '
                                      + str(len(self.__tickets)) + '.')
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
    """Main function"""

    ticket_system = TicketController()
    ticket_system.run()


if __name__ == '__main__':
    main()
