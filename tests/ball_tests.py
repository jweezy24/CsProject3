import unittest
import sys
import pong.ball as ball
import pong.player as player

class TestPlayerMethods(unittest.TestCase):
    def setUp(self):
        self.ball = ball.Ball()

    def test_init(self):
        self.assertTrue(self.ball.x != 0)
        self.assertTrue(self.ball.y != 0)
        self.assertTrue(self.ball.speed != 0)

    def test_reset_position_speed(self):
        self.ball.reset("R")
        self.assertTrue(self.ball.x == 400)
        self.assertTrue(self.ball.y == 350.0)
        self.assertTrue(self.ball.speed == 16.0)

    def test_reset_side_L(self):
        self.ball.reset("L")
        #self.direction = -45
        self.assertTrue(self.ball.direction == 45)
        self.assertTrue(self.ball.direction != -45)

    def test_reset_side_L(self):
        self.ball.reset("R")
        #self.direction = -45
        self.assertTrue(self.ball.direction != 45)
        self.assertTrue(self.ball.direction == -45)

    def test_wall_bounce(self):
        temp_holder = self.ball.direction
        #self.direction = (180-self.direction)%360
        self.ball.wall_bounce()
        self.assertTrue(self.ball.direction != temp_holder)
        self.assertTrue(self.ball.direction == (180-temp_holder)%360)

    def test_player_bounce_L(self):
        temp_player = player.Player(username='testler', side='L', pos=25)
        temp_direction = self.ball.direction
        self.ball.player_bounce(temp_player, 30)
        self.assertTrue(self.ball.direction != temp_direction)
        self.assertTrue(self.ball.direction == ((360-temp_direction)%360)-30)

    def test_player_bounce_R(self):
        temp_player = player.Player(username='testler', side='R', pos=775)
        temp_direction = self.ball.direction
        self.ball.player_bounce(temp_player, 30)
        self.assertTrue(self.ball.direction != temp_direction)
        self.assertTrue(self.ball.direction == ((360-temp_direction)%360)-30)

    # def test_update(self):
    #     holderRect = self.ball.rect.y
    #     holderY = self.ball.y
    #     self.assertTrue(self.ball.rect.y == holderRect)
    #     self.assertFalse(self.ball.rect.y != holderY)
    #     self.ball.update()
    #     self.assertTrue(self.ball.rect.y == holderY)

unittest.main()
