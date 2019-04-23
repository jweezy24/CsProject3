import server.Tree.BTree as BTree
import server.Tree.Node as Node

class Tournament:

    def __init__(self,size):
        self.size = size
        self.players = []
        self.matches = []

    def add_players(self, username, address):
        self.players.append(Node.Node([username, address]))

    def generate_matches(self):
        for i in range(0,players):
            if i%2 == 0:
                tempNode = Node(players[i].data[0] + " vs. " + players[i+1].data[0])
                tempNode.left = players[i]
                tempNode.right = players[i+1]
                self.matches.append(tempNode)
