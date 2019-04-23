import unittest
import sys
import pong.main_menu as menu
import shelve

class TestPlayerMethods(unittest.TestCase):
    def setUp(self):
        self.menu = menu

    def test_button(self):
        bright_red = (255,0,0)
        red = (200,0,0)
        def back_to_menu():
            return False

        self.assertTrue(self.menu.button("Test",200,200,200,200,red,bright_red,back_to_menu) == True)

    def test_shelve(self):
        d = shelve.open("userdetails", writeback=True)
        Username = d["username"]
        self.assertTrue(Username != "")

unittest.main()
    