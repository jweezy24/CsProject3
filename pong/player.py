import pygame


class Player:

    def __init__(self, username, ip, side):
        self.username = username
        self.ip = ip
        self.side = side
        self.position = 0
        self.score = 0

    def move(self, val):
        self.position += val

    def update_score(self):
        self.score+=1
