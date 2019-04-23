import unittest
import sys
import server.tournamentMode as Tournament

class TestTournamentMethods(unittest.TestCase):

    def setUp(self):
        self.tourny = Tournament.Tournament(4)

    def test_init(self):
        self.assertTrue(self.tourny.size == 4)
        self.assertTrue(self.tourny.players == [])

    def test_add_players(self):
        self.tourny.add_players("jweezy", ("127.0.0.1", 11111))
        self.assertTrue( self.tourny.players[0].data[0] == "jweezy")
        self.assertTrue(self.tourny.players[0].data[1][0] == "127.0.0.1")
        self.assertTrue(self.tourny.players[0].data[1][1] == 11111)


unittest.main()
