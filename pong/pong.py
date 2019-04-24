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

def send_start(game_server):
    global start
    sock2.settimeout(10)
    #print(game_server)
    while not start:
        try:
            sock.sendto("start".encode(), game_server)
            message,address = sock2.recvfrom(1024)
            if b"start" in message:
                start = True
        except Exception as e:
            print(e)

def send_info(json_message,game_server):
    print(str(game_server) + " send info")
    sock.sendto(str(json_message).encode(), game_server)

def send_victory(json_message):
    #print(game_server)
    game_server = ("<broadcast>", 7999)
    sock.sendto(str(json_message).encode(), game_server)

def create_listen_thread():
    t= threading.Thread(target=listen)
    threads.append(t)
    t.start()

def listen():
    global packet
    global start
    sock2.settimeout(10)
    print("created thread")
    while True:
        message, address = sock2.recvfrom(1024)
        #print(str(message) + " in pong listener" )
        if b'start' in message:
            start = True
        packet = str(message)



def pong(player1_name, player2_name, message, game_server):
    global packet
    global start
    global game_finished
    create_listen_thread()
    dict_message = {"op" :"update", "move": 0, "ball_x": 400, "ball_y": 350.0}
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

    while not exit_program and start:

        # Clear the screen
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                main_menu.quit()

        keys = pygame.key.get_pressed()  #checking pressed keys
        if keys[pygame.K_w]:
            dict_message["move"] = -10

        if keys[pygame.K_s]:
            dict_message["move"] = 10


        if 'update' in packet:
            ball_update = json.loads(packet.replace("b'", '').replace("'", ''))
            dict_message["ball_x"] = (ball.x + ball_update["ball_x"])/2
            dict_message["ball_y"] = (ball.y + ball_update["ball_y"])/2
        else:
            dict_message["ball_x"] = ball.x
            dict_message["ball_y"] = ball.y

        # Stop the game if there is an imbalance of 3 points\
        if abs(score1 - score2) > 2:
            if "tm" in message["op"]:
                victory_json = {"op":"tm_result", "winner":'', "loser":''}
            else:
                victory_json = {"op":"game_over", "winner":'', "loser":''}
            print("in victory packet")
            done = True
            #if the difference is positive then score1 won => player 1 victory
            if score1 - score2 > 0:
                if "tm" in message["op"]:
                    if local_username == player1_name:
                        victory_json.update({"winner":(player1_name, (message["username1"][1][0], sock2.getsockname()[1]))})
                    victory_json.update({"loser":player2_name})
                else:
                    victory_json.update({"winner":player1_name})
                    victory_json.update({"loser":player2_name})
                #we also only want to send the victory message once
                #to do this we make sure that the username local to the player is player1
                if local_username == player1_name:
                    send_victory(json.dumps(victory_json))
                    movingsprites.remove(player1)
                    movingsprites.remove(player2)
                    movingsprites.remove(ball)
                    balls.remove(ball)
                    score1 = 0
                    score2 = 0
                    del player1
                    del player2
                    del ball
                    time.sleep(2)
                    packet = ''
                    game_finished = True
                else:
                    pygame.quit()
                    sys.exit()
            else:
                if "tm" in message["op"]:
                    if local_username == player2_name:
                        victory_json.update({"winner":(player2_name, (message["username2"][1][0], sock2.getsockname()[1]))})
                    victory_json.update({"loser":player1_name})
                else:
                    victory_json.update({"winner":player2_name})
                    victory_json.update({"loser":player1_name})
                #we also only want to send the victory message once
                #to do this we make sure that the username local to the player is player1
                if local_username == player2_name:
                    send_victory(json.dumps(victory_json))
                    movingsprites.remove(player1)
                    movingsprites.remove(player2)
                    movingsprites.remove(ball)
                    balls.remove(ball)
                    score1 = 0
                    score2 = 0
                    del player1
                    del player2
                    del ball
                    time.sleep(2)
                    packet = ''
                    game_finished = True
                else:
                    pygame.quit()
                    sys.exit()
        if not done:
            # Update the player and ball positions
            send_info(json.dumps(dict_message),game_server)
            #print(packet + " packet")
            if 'update' in packet:
                #print("here")
                json_message = json.loads(packet.replace("b'", '').replace("'", ''))
                ball.x = dict_message['ball_x']
                ball.y = dict_message['ball_y']
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
                #print("packet not recieved")
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
    count = 0
    game_found = False
    message = "none"
    global local_username
    global previous_player
    global game_finished
    player_found = False
    while not game_found:
        if count == 0:
            game_found, message, username = main_menu.game_intro(sock,sock2,sock3)
            count = 1
        message = str(message)
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
            send_start(game_server)

        elif username == json_message["username2"][0] and player_found:
            game_found = True
            game_server = (json_message["username1"][1][0], json_message["username1"][1][1])
            send_start(game_server)

        else:
            continue


        if game_found:
            pong(json_message["username1"][0], json_message["username2"][0], json_message, game_server)
            if game_finished:
                game_over = False
                count = 0


if __name__ == '__main__':
    #while True:
    first_phase()
    pygame.quit()
