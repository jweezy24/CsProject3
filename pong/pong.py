# --- Import libraries used for this program

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
#init networking stuff
sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock2.bind(("0.0.0.0",0))
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
threads = []

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

def send_info(json_message,game_server):
    #print(game_server)
    sock.sendto(str(json_message).encode(), ('<broadcast>', game_server[1]))

def create_listen_thread():
    t= threading.Thread(target=listen)
    threads.append(t)
    t.start()

def listen():
    global packet
    while True:
        message, address = sock2.recvfrom(1024)
        #print(sock2.getsockname())
        packet = str(message)

def pong(player1_name, player2_name, message, game_server):
    global packet
    create_listen_thread()
    dict_message = {"op" :"update", "move": 0}
    BLACK = (0 ,0, 0)
    WHITE = (255, 255, 255)

    score1 = 0
    score2 = 0

    # Call this function so the Pygame library can initialize itself
    pygame.init()

    # Create an 800x600 sized screen
    screen = pygame.display.set_mode([800, 600])

    # Set the title of the window
    pygame.display.set_caption('Pong')

    # Enable this to make the mouse disappear when over our window
    pygame.mouse.set_visible(0)

    # This is a font we use to draw text on the screen (size 36)
    font = pygame.font.Font(None, 36)

    # Create a surface we can draw on
    background = pygame.Surface(screen.get_size())

    # Create the ball
    ball = ball2.Ball()
    # Create a group of 1 ball (used in checking collisions)
    balls = pygame.sprite.Group()
    balls.add(ball)


    # Create the player paddle object
    player1 = player.Player(player1_name,"L", 25)
    player2 = player.Player(player2_name,"R", 775)

    movingsprites = pygame.sprite.Group()
    movingsprites.add(player1)
    movingsprites.add(player2)
    movingsprites.add(ball)

    clock = pygame.time.Clock()
    done = False
    exit_program = False

    while not exit_program:

        # Clear the screen
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                main_menu.quit()

        keys = pygame.key.get_pressed()  #checking pressed keys
        if keys[pygame.K_w]:
            dict_message["move"] = 10
        if keys[pygame.K_s]:
            dict_message["move"] = -10


        # Stop the game if there is an imbalance of 3 points
        if abs(score1 - score2) > 3:
            done = True

        if not done:
            # Update the player and ball positions
            send_info(json.dumps(dict_message),game_server)
            #print(packet + " packet")
            if 'update' in packet:
                #print("here")
                json_message = json.loads(packet.replace("b'", '').replace("'", ''))
                if json_message['op'] == 'update':
                    #print("here")
                    json_message = json.loads(packet.replace("b'", '').replace("'", ''))
                    #print(local_username + "here")
                    if player1_name == local_username:
                        player1.move(dict_message['move'])
                        player2.move(json_message["move"])
                        player1.update()
                        player2.update()
                        ball.update()
                    else:
                        player2.move(dict_message['move'])
                        player1.move(json_message["move"])
                        player1.update()
                        player2.update()
                        ball.update()
            else:
                print("packet not recieved")
                if player1_name == local_username:
                    player1.move(dict_message['move'])
                else:
                    player2.move(dict_message['move'])
            dict_message['move'] = 0

        # If we are done, print game over
        if done:
            text = font.render("Game Over", 1, (200, 200, 200))
            textpos = text.get_rect(centerx=background.get_width()/2)
            textpos.top = 50
            screen.blit(text, textpos)

        # See if the ball hits the player paddle
        if pygame.sprite.spritecollide(player1, balls, False):
            # The 'diff' lets you try to bounce the ball left or right depending where on the paddle you hit it
            diff = (player1.rect.x + player1.width/2) - (ball.rect.x+ball.width/2)

            # Set the ball's y position in case we hit the ball on the edge of the paddle
            ball.player_bounce(player1,diff)

        # See if the ball hits the player paddle
        if pygame.sprite.spritecollide(player2, balls, False):
            # The 'diff' lets you try to bounce the ball left or right depending where on the paddle you hit it
            diff = (player2.rect.x + player2.width/2) - (ball.rect.x+ball.width/2)
            # Set the ball's y position in case we hit the ball on the edge of the paddle
            ball.player_bounce(player2,diff)

        # Print the score
        scoreprint = str(player1_name) + ": "+str(score1)
        text = font.render(scoreprint, 1, WHITE)
        textpos = (0, 0)
        screen.blit(text, textpos)

        scoreprint = str(player2_name) + ": "+str(score2)
        text = font.render(scoreprint, 1, WHITE)
        textpos = (300, 0)
        screen.blit(text, textpos)

        # Draw Everything
        movingsprites.draw(screen)

        # Update the screen
        pygame.display.flip()

        score1 = ball.p1_score
        score2 = ball.p2_score

        clock.tick(30)

def first_phase():
    game_found = False
    message = "none"
    global local_username
    while not game_found:
        game_found, message = main_menu.game_intro(sock,sock2,sock3)
        #print(message)
        if message != "none" or message != None:
            json_message = json.loads(message.replace("b'", '').replace("'", ''))
        if json_message['sleep'] == 1:
            time.sleep(.01)
        local_username = json_message['local_name']
        game_server = (json_message['player'][0], json_message['player'][1])
        pong(json_message["username_local"], json_message["username_away"], message, game_server)

if __name__ == '__main__':
    first_phase()
    pygame.quit()
