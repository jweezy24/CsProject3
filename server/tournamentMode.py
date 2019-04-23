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
            if self.player_in_game(username):
                return True
        return False

    def player_in_game(self, username):
        for i in self.matches:
            if username in i.data:
                return True
        return False

    def queue_up_next(self, player):
        tempNode = Node.Node(player[0] + "vs. waiting")
        tempNode.left = Node.Node(player)
        self.matches.append(tempNode)

    def generate_matches(self):
        i = 0
        while len(self.players) > 0:
            if i%2 == 0:
                tempP1 = self.players.pop()
                tempP2 = self.players.pop()
                tempNode = Node.Node(tempP1.data[0] + " vs. " + tempP2.data[0])
                tempNode.left = tempP1
                tempNode.right = tempP2
                self.matches.append(tempNode)
            if len(self.players)%2 == 1:
                if i+1 >= len(self.players):
                    tempP1 = self.players.pop()
                    tempNode = Node.Node(tempP1.data[0] + " vs. waiting" )
                    self.matches.append(tempNode)
            i+=1

        print("game 1: " + self.matches[0].data)
        print("game 2: " + self.matches[1].data)
