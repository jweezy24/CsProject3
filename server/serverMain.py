import socket
import time
import os
import sys
import json
import csv
import threading
import struct
import argparse
import server.tournamentMode as tourny

class match_maker:
    def __init__(self):
        #self.server_address = 'localhost'
        self.connection = None
        self.lobbies = []
        self.player_queue = []
        self.threads = []
        self.tournament = None
        self.isTourny = False
        self.tourny_size = 0
        self.init_network()

    def init_network(self):
        #get multicast address linux netstat -anu|sort -nk4
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind(('0.0.0.0',7999))
        self.lobby_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.lobby_socket.bind(('0.0.0.0',8001))
        self.MCAST_GRP = '224.0.0.251'
        self.MCAST_PORT = 5007
        self.cast_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.cast_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)

    def create_tournament(self):
        self.tournament = tourny.Tournament(self.tourny_size)

    def add_player_to_tourny(self, player, address):
        self.tournament.add_players(player, address)

    def generate_bracket(self):
        self.tournament.generate_matches()
        print(self.tournament.matches)

    def listen(self):
        message = ''
        address = ''
        #creates a tournament object
        if self.isTourny:
            self.create_tournament()
        try:
            message, address = self.server_socket.recvfrom(1024)
            if len(self.player_queue) >= 2 and not self.isTourny:
                self.match_players()
                time.sleep(1)
            elif len(self.player_queue) >= self.tourny_size and self.isTourny:
                self.generate_bracket()

        except socket.timeout:
            print("timeout")
            return
        self.parse_json(message,address)

    def parse_json(self,packet,address):
        try:
            print(address)
            json_message = json.loads(packet)
            if json_message["op"] == "searching" and not self.player_in_queue(json_message['username']) and not self.isTourny:
                self.player_queue.append((json_message["username"], json_message, (address[0], json_message["port"])))
                if self.new_player(json_message["username"]):
                    self.write_player_to_memory(json_message["username"])
            if json_message["op"] == "searching" and not self.player_in_queue(json_message['username']) and self.isTourny:
                self.add_player_to_tourny(json_message["username"], (address[0], json_message["port"]))
                if self.new_player(json_message["username"]):
                    self.write_player_to_memory(json_message["username"])
            if json_message["op"] == "game_over":
                print("got packet to update winrate")
                self.update_winrate(json_message["winner"], json_message["loser"])


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
        writer.writerow(["username", name, "rank", 0,"games",0,"winrate",0,"wins",0])
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

    def update_winrate(self, winner, loser):
        rows = []
        old_csv = open('./allPlayers.csv', newline='')
        reader = csv.reader(old_csv)
        for row in reader:
            rows.append(row)
        old_csv.close()
        csv_file = open('./allPlayers.csv', 'w', newline='')
        writer = csv.writer(csv_file)
        for i in range(0,len(rows)):
            if rows[i][1] == winner:
                #adding the game to the user
                print(rows[i][5])
                rows[i][5] = str(int(rows[i][5])+1)
                #adding a win for the user
                rows[i][9] = str(int(rows[i][9])+1)
                #writing the winrate up to two decimal places
                rows[i][7] = float("{0:.2f}".format(float(int(rows[i][9]) / int(rows[i][5]))))
        for i in rows:
            writer.writerow(i)
        csv_file.close()



    def play_game(self,player1, player2):
        dict = {"op":" match made ", "username1": (player1[0], player1[2]), "username2": (player2[0], player2[2])}
        send_out_1 = json.dumps(dict)
        self.cast_sock.sendto(send_out_1.encode(), (self.MCAST_GRP, self.MCAST_PORT))

if __name__ == '__main__':
    server = match_maker()
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-t', help='To create a tournament -t <size of tourny>')
    options = vars(parser.parse_args())
    while True:
        if options['t']:
            server.isTourny = True
            server.tourny_size = int(options['t'])
            server.listen()
        else:
            print("no tourny")
            server.listen()
