"""Test two functions in the main to make sure there is no bug in the system"""

import unittest
from ticketViewer.main import TicketController


class TestModel(unittest.TestCase):

    def test_is_pos(self):
        controller = TicketController()
        self.assertFalse(controller._TicketController__is_pos('-1'))
        self.assertFalse(controller._TicketController__is_pos('0'))
        self.assertFalse(controller._TicketController__is_pos('sldjfs'))
        self.assertFalse(controller._TicketController__is_pos('-0'))
        self.assertFalse(controller._TicketController__is_pos('84a'))
        self.assertFalse(controller._TicketController__is_pos('0.1'))
        self.assertTrue(controller._TicketController__is_pos('6'))
        self.assertTrue(controller._TicketController__is_pos('248204'))

    def test_is_page_changer(self):
        controller = TicketController()
        self.assertFalse(controller._TicketController__is_page_changer("-1", 9))
        self.assertFalse(controller._TicketController__is_page_changer("1.5", 7))
        self.assertFalse(controller._TicketController__is_page_changer("8", 7))
        self.assertFalse(controller._TicketController__is_page_changer("0", 6))
        self.assertFalse(controller._TicketController__is_page_changer("abc", 9))
        self.assertFalse(controller._TicketController__is_page_changer("p-1", 9))
        self.assertFalse(controller._TicketController__is_page_changer("p1.5", 7))
        self.assertFalse(controller._TicketController__is_page_changer("p8", 7))
        self.assertFalse(controller._TicketController__is_page_changer("p0", 6))
        self.assertFalse(controller._TicketController__is_page_changer("pabc", 9))
        self.assertTrue(controller._TicketController__is_page_changer("p1", 8))
        self.assertTrue(controller._TicketController__is_page_changer("p9", 9))
        self.assertTrue(controller._TicketController__is_page_changer("p6", 9))
        
if __name__ == '__main__':
    unittest.main()