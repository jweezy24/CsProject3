# --- Import libraries used for this program
# get multicast addresses netstat -anu|sort -nk4
import sys
import math
import pygame
import random
import player
import ball as ball2
import socket
import main_menu
import json
import threading
import time
import pong_main_thread
#init networking stuff
sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock2.bind(("0.0.0.0",0))
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
threads = []

next_round = False
start = False
game_finished = False
previous_player = ''

MCAST_GRP = '224.0.0.251'
MCAST_PORT = 5007
sock3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
try:
    sock3.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
except AttributeError:
    pass
sock3.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
sock3.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)

sock3.bind((MCAST_GRP, MCAST_PORT))
host = socket.gethostbyname(socket.gethostname())
sock3.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton(host))
sock3.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP,
               socket.inet_aton(MCAST_GRP) + socket.inet_aton(host))



local_username = ''
packet = ''



def main():
    count = 0
    game_found = False
    message = "none"
    global local_username
    global previous_player
    global game_finished
    player_found = False
    while True:
        time.sleep(2)
        if count == 0:
            game_found, message, username = main_menu.game_intro(sock2,sock,sock3)
            count = 1
        message = str(message)
        print(message)
        if message != "none" or message != None:
            json_message = json.loads(message.replace("b'", '').replace("'", ''))

        local_username = username
        if previous_player != json_message["username1"][0] and json_message["username2"][0] != local_username:
            previous_player = json_message["username1"][0]
            player_found = True
            #print(previous_player + " is the previous_player")

        elif previous_player != json_message["username2"][0] and json_message["username1"][0] != local_username:
            previous_player = json_message["username2"][0]
            player_found = True

        if username == json_message["username1"][0] and player_found:
            game_found = True
            game_server = (json_message["username2"][1][0], json_message["username2"][1][1])
            #send_start(game_server)

        elif username == json_message["username2"][0] and player_found:
            game_found = True
            game_server = (json_message["username1"][1][0], json_message["username1"][1][1])
            #send_start(game_server)

        else:
            continue


        if game_found:
            game = pong_main_thread.pong_main_thread(json_message["username1"][0], json_message["username2"][0], json_message, game_server)
            game.init_network(sock, sock2, sock3, game_server)
            game.set_local_username(local_username)
            game.sender.send_start()
            game.start()
            game.join()
            if game.game_finished:
                del game
                count = 0
                game_found = False

if __name__ == '__main__':
    main()
    pygame.quit()
