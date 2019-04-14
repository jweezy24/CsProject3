import math
import pygame
import random
import player as Player

# Define some colors
BLACK = (0 ,0, 0)
WHITE = (255, 255, 255)
class Player(pygame.sprite.Sprite):

    def __init__(self, username, side, pos):
        self.username = username
        self.side = side
        self.position = pos
        self.score = 0
        self.width = 15
        self.height = 75
        super().__init__()

        # Create the image of the ball
        self.image = pygame.Surface([15, 75])

        # Color the ball
        self.image.fill(WHITE)

        # Get a rectangle object that shows where our image is
        self.rect = self.image.get_rect()

        self.y = self.rect.y
        self.rect.x = pos
        self.x = self.rect.x

    def move(self, movement):
        self.y += movement

    def update(self):
        self.rect.y = self.y

    def update_score(self):
        self.score+=1
