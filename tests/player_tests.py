import unittest
import sys
sys.path.insert(0, '../pong')
import player
class TestPlayerMethods(unittest.TestCase):
    def setUp(self):
        self.player = player.Player('test','L', 100)

    def test_init(self):
        self.assertTrue(self.player.username == 'test')
        self.assertTrue(self.player.side == 'L')
        self.assertTrue(self.player.position == 100)


unittest.main()
