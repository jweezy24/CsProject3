import socket
import time
import os
import sys
import json
import csv

class match_maker:
    def __init__(self):
        #self.server_address = 'localhost'
        self.connection = None
        self.lobbies = []
        self.player_queue = []
        self.threads = []
    def init_network(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind(('0.0.0.0',7999))

    def listen(self):
        message = ''
        address = ''
        try:
            message, address = self.server_socket.recvfrom(1024)
        except socket.timeout:
            print("timeout")
            return
        self.parse_json(message)

    def parse_json(self,packet):
        try:
            json_message = json.loads(packet)
            if json_message["op"] == "searching":
                player_queue.append((json_message["username"], json_message))

        except NameError:
            print('Incorrect Json format')

    def new_player(self, name):
        pass
