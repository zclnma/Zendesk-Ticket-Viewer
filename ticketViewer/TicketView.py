import time

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
        print('You can quit ticket viewer by entering "quit" at anytime.')
        print()
        print('-----------------------------------------------------------------')
        print()
        time.sleep(1)

    @classmethod
    def quit_system_message(cls):
        """message appears when ticket viewer system exits"""
        print('Thanks for using ticket viewer.')

    @classmethod
    def invalid_input_message(cls):
        print()
        print('Invalid input.')
        time.sleep(0.5)

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

