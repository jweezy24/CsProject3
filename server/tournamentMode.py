import server.Tree.BTree as BTree
import server.Tree.Node as Node

class Tournament:

    def __init__(self,size):
        self.size = size
        self.players = []
        self.matches = []

    def add_players(self, username, address):
        tempNode = Node.Node([username, address])
        self.players.append(tempNode)

    def get_total_players(self):
        return len(self.players)

    def player_in_tournament(self, username):
        for i in self.players:
            if i.data[0] == username:
                return True
        return False

    def generate_matches(self):
        for i in range(0, len(self.players)):
            if i%2 == 0:
                tempNode = Node.Node(self.players[i].data[0] + " vs. " + self.players[i+1].data[0])
                tempNode.left = self.players[i]
                tempNode.right = self.players[i+1]
                self.matches.append(tempNode)
