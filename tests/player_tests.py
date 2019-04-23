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
        holderRect = self.player.rect.y
        holderY = self.player.y
        self.assertTrue(self.player.rect.y == holderRect)
        self.assertFalse(self.player.rect.y != holderY)
        self.player.update()
        self.assertTrue(self.player.rect.y == holderY)

    def test_update_score(self):
        holder = self.player.score
        self.assertTrue(self.player.score == holder)
        self.player.update_score()
        self.assertTrue(self.player.score == holder+1)

unittest.main()
