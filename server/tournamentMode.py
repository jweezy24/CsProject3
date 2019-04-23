import server.Tree.BTree as BTree
import server.Tree.Node as Node

class Tournament:

    def __init__(self,size,players):
        self.size = size
        self.players = players
        self.matches = []

    def generate_bracket(self):
        pass

    def generate_matches(self):
        for i in range(0,players):
            if i%2 == 0:
                tempNode = Node(str(i/2))
                tempNode.left = Node(players[i])
                tempNode.right = Node(players[i+1])
