import socket
import time
import os
import sys
import json
import csv
import threading

class match_maker:
    def __init__(self):
        #self.server_address = 'localhost'
        self.connection = None
        self.lobbies = []
        self.player_queue = []
        self.threads = []
        self.init_network()
    def init_network(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind(('0.0.0.0',7999))
        self.lobby_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.lobby_socket.bind(('0.0.0.0',8001))

    def listen(self):
        message = ''
        address = ''
        try:
            message, address = self.server_socket.recvfrom(1024)
            if len(self.player_queue) >= 2:
                self.match_players()
        except socket.timeout:
            print("timeout")
            return
        self.parse_json(message,address)

    def parse_json(self,packet,address):
        try:
            json_message = json.loads(packet)
            if json_message["op"] == "searching" and not self.player_in_queue(json_message['username']):
                self.player_queue.append((json_message["username"], json_message, (address[0], json_message["port"][1])))
                if self.new_player(json_message["username"]):
                    self.write_player_to_memory(json_message["username"])


        except NameError:
            print('Incorrect Json format')

    def new_player(self, name):
        file = open('./allPlayers.csv')
        reader = csv.reader(file)
        for row in reader:
            for i in row:
                if name == i:
                    file.close()
                    return False
        file.close()
        return True


    def write_player_to_memory(self, name):
        rows = []
        old_csv = open('./allPlayers.csv', newline='')
        reader = csv.reader(old_csv)
        for row in reader:
            rows.append(row)
        old_csv.close()
        csv_file = open('./allPlayers.csv', 'w', newline='')
        writer = csv.writer(csv_file)
        for i in rows:
            writer.writerow(i)
        writer.writerow(["username", name, "rank", 0])
        csv_file.close()

    def player_in_queue(self, name):
        for i in self.player_queue:
            if i[0] == name:
                return True
        return False

    def match_players(self):
        print(self.player_queue)
        if len(self.player_queue) >=2:
            self.create_lobby(self.player_queue.pop(), self.player_queue.pop())

    def create_lobby(self, player1, player2):
        t = threading.Thread(target=self.play_game, args=(player1,player2, ))
        print(player1[2])
        self.threads.append(t)
        self.lobbies.append(("playing", player1, player2))
        t.start()


    #commented out central server model
    # def play_game(self, player1, player2):
    #     dict = {"op":" match made ", "player": player2[2], "username_local": player1[0], "username_away": player2[0] }
    #     dict2 = {"op":" match made ", "player": player1[2], "username_local": player2[0], "username_away": player1[0]}
    #     json_message = json.dumps(dict)
    #     json_message2 = json.dumps(dict2)
    #     print(player1)
    #     print(player2)
    #     self.server_socket.sendto(json_message2.encode(), player1[2])
    #     print("one mesage sent")
    #     self.server_socket.sendto(json_message.encode(), player2[2])
    #     print("second message sent")
    #     while True:
    #         send_out = {'local_movement': 0, 'away_movement': 0}
    #         message, address = self.lobby_socket.recvfrom(1024)
    #         json_message = json.loads(message)
    #         if address == player1[2]:
    #             send_out["away_movement"] = int(json_message["move"])
    #             json_message_temp = json.dumps(send_out)
    #             self.lobby_socket.sendto(json_message_temp.encode(), player2[2])
    #             send_out["away_movement"] = 0
    #             send_out["local_movement"] = int(json_message["move"])
    #             json_message_temp = json.dumps(send_out)
    #             self.lobby_socket.sendto(json_message_temp.encode(), player1[2])

    def play_game(self,player1, player2):
        dict = {"op":" match made ", "player": player2[2], "username_local": player1[0], "username_away": player2[0]}
        dict2 = {"op":" match made ", "player": player1[2], "username_local": player2[0], "username_away": player1[0]}
        send_out_1 = json.dumps(dict)
        send_out_2 = json.dumps(dict2)
        print(self.lobbies)
        self.lobby_socket.sendto(send_out_1.encode(), player1[2])
        self.lobby_socket.sendto(send_out_2.encode(), player2[2])

server = match_maker()

while True:
    server.listen()
