import unittest
import sys
import server.serverMain as server

class TestServerMethods(unittest.TestCase):
    def setUp(self):
        self.server = server.match_maker()

    def tearDown(self):
        self.server.tear_down_network()
        if not self.server.new_player("Dbangz"):
            self.server.remove_player_from_memory("Dbangz")
        if self.server.new_player("jweezy"):
            self.server.write_player_to_memory("jweezy")

    def test_init(self):
        self.assertTrue(not self.server.isTourny)
        self.assertFalse(self.server.connection)
        self.assertFalse(self.server.tournament)
        self.assertTrue(self.server.tourny_size == 0)

    def test_create_tournament(self):
        self.server.tourny_size = 2
        self.server.create_tournament()
        self.assertTrue(self.server.tournament)
        self.assertTrue(self.server.tournament.size == 2)

    def test_add_player_to_tourny(self):
        self.server.tourny_size = 2
        self.server.create_tournament()
        self.server.add_player_to_tourny("jweezy", ("127.1.2.3", 11111))
        self.assertTrue(self.server.tournament.get_total_players() == 1)
        self.assertTrue(self.server.tournament.player_in_tournament("jweezy"))

    def test_generate_bracket(self):
        self.server.tourny_size = 2
        self.server.create_tournament()
        self.server.add_player_to_tourny("jweezy", ("127.1.2.3", 11111))
        self.server.add_player_to_tourny("jweezy2", ("127.1.2.5", 11112))
        self.server.generate_bracket()
        self.assertTrue(self.server.tournament.matches[0].data == "jweezy2 vs. jweezy")

    def test_new_player(self):
        self.assertFalse(self.server.new_player("jweezy"))
        self.assertTrue(self.server.new_player("Dbangz"))

    def test_write_player_to_memory(self):
        self.assertFalse(self.server.new_player("jweezy"))
        self.assertTrue(self.server.new_player("Dbangz"))
        self.server.write_player_to_memory("Dbangz")
        self.assertFalse(self.server.new_player("Dbangz"))

    def test_remove_player_from_memory(self):
        self.assertFalse(self.server.new_player("jweezy"))
        self.server.remove_player_from_memory("jweezy")
        self.assertTrue(self.server.new_player("jweezy"))

    def test_player_in_queue(self):
        self.server.player_queue.append(("jweezy", ['127.0.0.1', 11111]))
        self.assertTrue(self.server.player_in_queue("jweezy"))
        self.assertFalse(self.server.player_in_queue("Dbangz"))



unittest.main()
