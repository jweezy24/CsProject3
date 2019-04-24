import unittest
import sys
import server.tournamentMode as Tournament
import server.Tree.Node as Node

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

    def test_get_total_players(self):
        self.assertTrue(len(self.tourny.players) == self.tourny.get_total_players())

    def test_player_in_tournament(self):
        self.tourny.add_players("jweezy", ("127.0.0.1", 11111))
        self.assertTrue(self.tourny.player_in_tournament("jweezy"))

    def test_queue_up_next_player(self):
        self.tourny.queue_up_next(("jweezy", ("127.0.0.1", 11111)))
        self.assertTrue(self.tourny.matches[0].data == "jweezyvs. waiting")
        self.assertTrue(self.tourny.matches[0].left.data == Node.Node(("jweezy", ("127.0.0.1", 11111))).data)
        self.assertTrue(self.tourny.matches[0].right == None)

    def test_genereate_matches(self):
        self.tourny.add_players("jweezy", ("127.0.0.2", 11112))
        self.tourny.add_players("jweezy2", ("127.0.0.3", 11113))
        self.tourny.add_players("jweezy3", ("127.0.0.4", 11114))
        self.tourny.generate_matches()
        self.assertTrue(self.tourny.matches[0].data == "jweezy3 vs. jweezy2")
        self.assertTrue(self.tourny.matches[1].data == "jweezy vs. waiting")

    def test_player_in_game(self):
        self.tourny.add_players("jweezy", ("127.0.0.2", 11112))
        self.tourny.add_players("jweezy2", ("127.0.0.3", 11113))
        self.tourny.add_players("jweezy3", ("127.0.0.4", 11114))
        self.tourny.generate_matches()
        self.assertTrue(self.tourny.player_in_game("jweezy"))
        self.assertFalse(self.tourny.player_in_game("allyssa"))



unittest.main()
