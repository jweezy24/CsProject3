import unittest
import sys
import server.tournamentMode as Tournament

class TestTournamentMethods(unittest.TestCase):

    def setUp(self):
        self.tourny = Tournament.Tournament(4,["1","2","3","4"])

    def test_init(self):
        self.assertTrue(self.tourny.size == 4)
        self.assertTrue(self.tourny.players == ["1","2","3","4"])


unittest.main()
