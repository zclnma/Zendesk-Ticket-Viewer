import time
import sys

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
