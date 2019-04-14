import unittest
import sys
import pong.player as player
class TestPlayerMethods(unittest.TestCase):
    def setUp(self):
        self.player = player.Player('test','L', 100)

    def test_init(self):
        self.assertTrue(self.player.username == 'test')
        self.assertTrue(self.player.side == 'L')
        self.assertTrue(self.player.position == 100)

    def test_move(self):
        holder = self.player.y
        self.assertTrue(self.player.y == holder)
        self.player.move(10)
        self.assertTrue(self.player.y == holder+10)

    def test_update(self):
        pass


unittest.main()
