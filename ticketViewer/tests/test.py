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

    def test_is_number_valie(self):
        controller = TicketController()
        self.assertTrue(controller._TicketController__number_valid(25, 2, 3, 25, 101))
        self.assertTrue(controller._TicketController__number_valid(1, 2, 4, 25, 101))
        self.assertTrue(controller._TicketController__number_valid(15, 1, 3, 25, 101))
        self.assertTrue(controller._TicketController__number_valid(17, 2, 3, 28, 101))
        self.assertTrue(controller._TicketController__number_valid(1, 2, 3, 33, 101))
        self.assertFalse(controller._TicketController__number_valid(0, 2, 3, 25, 101))
        self.assertFalse(controller._TicketController__number_valid(2348, 2, 3, 25, 101))
        self.assertFalse(controller._TicketController__number_valid(26, 2, 3, 25, 101))
        self.assertFalse(controller._TicketController__number_valid(2, 5, 5, 25, 101))
        self.assertFalse(controller._TicketController__number_valid(0, 2, 3, 25, 101))

if __name__ == '__main__':
    unittest.main()