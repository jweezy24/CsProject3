import socket
import threading
import time
import game_threads
import pygame
import ball as ball2
import player
import json
import sys

class pong_main_thread(threading.Thread):

    def __init__(self, player1_name, player2_name, message, game_server):
        threading.Thread.__init__(self)
        self.packet = ''
        self.game_finished = False
        self.local_username = ''
        self.daemon = False
        self.game_server = game_server
        self.message = message
        self.player2_name = player2_name
        self.player1_name = player1_name
        self.communicator = None

    def init_network(self, sock, sock2, sock3, game_server):
        self.communicator = game_threads.reciever(sock2)
        self.sender = game_threads.sender(sock, game_threads.reciever(sock2), game_server)
        self.sender.daemon = False

    def set_local_username(self, name):
        self.local_username = name

    def run(self):
        self.communicator.start()
        self.sender.start()
        #self.sender.send_start()
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
        player1 = player.Player(self.player1_name,"L", 25)
        player2 = player.Player(self.player2_name,"R", 775)

        movingsprites = pygame.sprite.Group()
        movingsprites.add(player1)
        movingsprites.add(player2)
        movingsprites.add(ball)

        clock = pygame.time.Clock()
        done = False
        exit_program = False

        while not exit_program and self.sender.begin:

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


            if 'update' in self.communicator.packet:
                ball_update = json.loads(self.communicator.packet.replace("b'", '').replace("'", ''))
                dict_message["ball_x"] = (ball.x + ball_update["ball_x"])/2
                dict_message["ball_y"] = (ball.y + ball_update["ball_y"])/2
            else:
                dict_message["ball_x"] = ball.x
                dict_message["ball_y"] = ball.y

            # Stop the game if there is an imbalance of 3 points\
            if abs(score1 - score2) > 2:
                if "tm" in self.message["op"]:
                    victory_json = {"op":"tm_result", "winner":'', "loser":''}
                else:
                    victory_json = {"op":"game_over", "winner":'', "loser":''}
                print("in victory self.communicator.packet")
                done = True
                #if the difference is positive then score1 won => player 1 victory
                if score1 - score2 > 0:
                    if "tm" in self.message["op"]:
                        if self.local_username == self.player1_name:
                            victory_json.update({"winner":(self.player1_name, (message["username1"][1][0], self.sender.sender.getsockname()[1]))})
                        victory_json.update({"loser":self.player2_name})
                    else:
                        victory_json.update({"winner":self.player1_name})
                        victory_json.update({"loser":self.player2_name})
                    #we also only want to send the victory message once
                    #to do this we make sure that the username local to the player is player1
                    if self.local_username == self.player1_name:
                        self.sender.send_victory(json.dumps(victory_json))
                        movingsprites.remove(player1)
                        movingsprites.remove(player2)
                        movingsprites.remove(ball)
                        balls.remove(ball)
                        score1 = 0
                        score2 = 0
                        exit_program = True
                        self.game_finished = True
                    else:
                        pygame.quit()
                        sys.exit()
                else:
                    if "tm" in self.message["op"]:
                        if self.local_username == self.player2_name:
                            victory_json.update({"winner":(self.player2_name, (self.message["username2"][1][0], self.sender.sender.getsockname()[1]))})
                        victory_json.update({"loser":self.player1_name})
                    else:
                        victory_json.update({"winner":self.player2_name})
                        victory_json.update({"loser":self.player1_name})
                    #we also only want to send the victory message once
                    #to do this we make sure that the username local to the player is player1
                    if self.local_username == self.player2_name:
                        self.sender.send_victory(json.dumps(victory_json))
                        movingsprites.remove(player1)
                        movingsprites.remove(player2)
                        movingsprites.remove(ball)
                        balls.remove(ball)
                        score1 = 0
                        score2 = 0
                        exit_program = True
                        self.game_finished = True
                    else:
                        pygame.quit()
                        sys.exit()
            if not done:
                # Update the player and ball positions
                self.sender.send_info(json.dumps(dict_message))
                #print(packet + " packet")
                if 'update' in self.communicator.packet:
                    #print("here")
                    json_message = json.loads(self.communicator.packet.replace("b'", '').replace("'", ''))
                    ball.x = dict_message['ball_x']
                    ball.y = dict_message['ball_y']
                    if json_message['op'] == 'update':
                        #print("here")
                        json_message = json.loads(self.communicator.packet.replace("b'", '').replace("'", ''))
                        #print(local_username + "here")
                        if self.player1_name == self.local_username:
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
                    if self.player1_name == self.local_username:
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
            scoreprint = str(self.player1_name) + ": "+str(score1)
            text = font.render(scoreprint, 1, WHITE)
            textpos = (0, 0)
            screen.blit(text, textpos)

            scoreprint = str(self.player2_name) + ": "+str(score2)
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
