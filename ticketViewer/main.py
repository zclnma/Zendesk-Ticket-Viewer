"""This module can retrieve tickets from Zendesk website with username&password access
    and allow users to view those tickets in CLI
        14/06/2018 -- Lionel
"""

import sys
import base64
import time
import math
import configparser

from ticketViewer.TicketModel import TicketModel
from ticketViewer.TicketView import TicketView

class TicketController:
    """Main system running"""

    def __init__(self):
        """Define variables"""
        self.__url = 'default'
        self.__username = 'default'
        self.__password = 'default'
        self.__item_per_page = 0
        self.__tickets = []
        self.model = TicketModel()
        self.view = TicketView()

    def __read_config(self):
        try:
            config = configparser.RawConfigParser()
            config.read('config.txt')
            self.__url = config.get('configuration', 'url')
            self.__username = config.get('configuration', 'username')
            self.__password = config.get('configuration', 'password')
            self.__item_per_page = int(config.get('configuration', 'item_per_page'))
        except:
            print('Unable to read configuration file.')
            time.sleep(0.5)
            print('Exiting...')
            time.sleep(0.5)
            sys.exit()

    @classmethod
    def __base64_auth(cls, auth_str):
        """base64 authenticate a string"""
        auth = base64.b64encode(auth_str.encode('utf-8')).decode('utf-8')
        return auth

    @classmethod
    def __is_pos(cls, input_str):
        """check if a string is positive or not"""
        try:
            input_str = int(input_str)
            if input_str > 0:
                return isinstance(input_str, int)
        except:
            return False
        else:
            return False

    def __is_page_changer(self, input_str, total_page):
        """"check if a string is a page changer of not
        eligible page changer should start with p followed by number less than total page"""

        if input_str.startswith('p') and self.__is_pos(input_str[1:]):
            if 0 < int(input_str[1:]) <= total_page:
                return True
            return False
        return False

    def run(self):
        """System starts"""

        ##1.read config file
        self.__read_config()

        ##2.auth string after base64 authentication
        auth = self.__base64_auth('%s:%s' % (self.__username, self.__password))


        ##3. Retrieve tickets from the server
        self.model.retrieve_ticket(self.__url, auth)

        ##4. Get tickets from the model and update tickets in the view
        self.__tickets = self.model.get_tickets()
        self.view.update_tickets_in_view(self.__tickets)

        ##5. Show system startup message
        self.view.startup_message()

        ##6. Start the ticket viewer system
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

                            elif self.__is_pos(detail_or_change_page):
                                #check if input is valid
                                if ((0 < int(detail_or_change_page) <= self.__item_per_page)
                                        and (current_page != total_page)) \
                                        or (0 < (int(detail_or_change_page) + (total_page - 1) * self.__item_per_page - 1
                                             < len(self.__tickets))
                                            and(current_page == total_page)):

                                    self.view.view_ticket_detail(
                                        int(detail_or_change_page) + self.__item_per_page * (current_page - 1)
                                    )
                                    back_from_detail = True
                                    continue

                                else:
                                    self.view.invalid_input_message()
                                    continue

                            elif self.__is_page_changer(detail_or_change_page, total_page):
                                current_page = int(detail_or_change_page[1:])
                                back_from_detail = False
                                print()
                                continue

                            else:
                                self.view.invalid_input_message()
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
                            elif self.__is_pos(selected_ticket):
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


def main(argv):
    """Main function"""
    ticket_system = TicketController()
    ticket_system.run()

if __name__ == '__main__':
    main(sys.argv)
