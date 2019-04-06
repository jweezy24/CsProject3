import pygame
import time
import random
import socket
import csv
import json
import threading

#most code is from here https://pythonprogramming.net/pygame-start-menu-tutorial/
pygame.init()

display_width = 800
display_height = 600

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

block_color = (53,115,255)


gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Pong')
clock = pygame.time.Clock()
threads = []
local_server = ("<broadcast>", 7999)



def read_csv():
    file = open('./config.csv')
    reader = csv.reader(file)
    username = 'NOT_FOUND'
    val_found = False
    for row in reader:
        for item in row:
            if item == 'username':
                val_found = True
                continue
            if val_found:
                username = item
                val_found = False
    file.close()
    return username


def send_info(sock, sock2):
    username = read_csv()
    print(username)
    dict = {'op': 'searching', 'username': username, 'port':sock2.getsockname()[1]}
    json_message = json.dumps(dict)
    sock.sendto(str(json_message).encode(), local_server)

def create_listen_thread(sock):
    t= threading.Thread(target=listen, args=(sock, ))
    threads.append(t)
    t.start()

def listen(sock):
    while True:
        message, address = sock.recvfrom(1024)
        threads[0].name = message

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def button(msg,x,y,w,h,ic,ac,action):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))

        if click[0] == 1:
                return action()
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("freesansbold.ttf",30)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)
    return True

def back_to_menu():
    return False

def settingsloop():

    bright_red = (255,0,0)
    red = (200,0,0)
    settings = True

    while settings:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        largeText = pygame.font.Font('freesansbold.ttf',115)
        TextSurf, TextRect = text_objects("Settings", largeText)
        TextRect.center = ((display_width/2),(display_height/4))
        gameDisplay.blit(TextSurf, TextRect)

        mouse = pygame.mouse.get_pos()

        settings = button("Back",(display_width/2)-100,280,200,50,red,bright_red,back_to_menu)

        pygame.display.update()
        clock.tick(15)

    return True

def start():
    return False

def menu():

    intro = True
    green = (0,200,0)
    bright_green = (0,255,0)

    while intro:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        largeText = pygame.font.Font('freesansbold.ttf',115)
        TextSurf, TextRect = text_objects("Pong Online", largeText)
        TextRect.center = ((display_width/2),(display_height/4))
        gameDisplay.blit(TextSurf, TextRect)

        mouse = pygame.mouse.get_pos()

        button("Settings",(display_width/2)-100,400,200,50,green,bright_green,settingsloop)
        intro = button("Start",(display_width/2)-100,340,200,50,green,bright_green,start)

        pygame.display.update()
        clock.tick(15)

    return (intro)

def game_intro(sock,sock2):
    create_listen_thread(sock2)
    count = 0
    intro = True
    display_searchRect = None
    display_searchSurf = None
    while intro:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)
        largeText = pygame.font.Font('freesansbold.ttf',85)
        medText = pygame.font.Font('freesansbold.ttf',35)
        TextSurf, TextRect = text_objects("Pong", largeText)
        TextSurfS1, TextRectS1 = text_objects("Searching", medText)
        TextSurfS2, TextRectS2 = text_objects("Searching.", medText)
        TextSurfS3, TextRectS3 = text_objects("Searching..", medText)
        TextSurfS4, TextRectS4 = text_objects("Searching...", medText)
        TextRect.center = ((display_width/2),(display_height/2))
        TextRectS4.center = (199, 555)
        TextRectS3.center = (164, 555)
        TextRectS2.center = (129, 555)
        TextRectS1.center = (94, 555)
        gameDisplay.blit(TextSurf, TextRect)
        if count%16 == 2:
            gameDisplay.blit(TextSurfS4, TextRectS4)
            display_searchRect = TextRectS4
            display_searchSurf = TextSurfS4
        elif count%16 == 5:
            gameDisplay.blit(TextSurfS3, TextRectS3)
            display_searchRect = TextRectS3
            display_searchSurf = TextSurfS3
        elif count%16 == 9:
            gameDisplay.blit(TextSurfS2, TextRectS2)
            display_searchRect = TextRectS2
            display_searchSurf = TextSurfS2
        elif count%16 == 13:
            gameDisplay.blit(TextSurfS1, TextRectS1)
            display_searchRect = TextRectS1
            display_searchSurf = TextSurfS1
        else:
            if display_searchRect != None:
                gameDisplay.blit(display_searchSurf,display_searchRect)
        send_info(sock,sock2)
        message = threads[0].name
        if "match made" in message:
            return(True, message)

        pygame.display.update()
        clock.tick(15)
        count+=1
