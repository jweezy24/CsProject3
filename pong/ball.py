import math
import pygame
import random

# Define some colors
BLACK = (0 ,0, 0)
WHITE = (255, 255, 255)
# This class represents the ball
# It derives from the "Sprite" class in Pygame
class Ball(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block, and its x and y position
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Create the image of the ball
        self.image = pygame.Surface([10, 10])

        # Color the ball
        self.image.fill(WHITE)

        # Get a rectangle object that shows where our image is
        self.rect = self.image.get_rect()

        # Get attributes for the height/width of the screen
        try:
            self.screenheight = pygame.display.get_surface().get_height()
            self.screenwidth = pygame.display.get_surface().get_width()
        except Exception as e:
            print(e)
            self.screenwidth = 800

        # Speed in pixels per cycle
        self.speed = 0

        # Floating point representation of where the ball is
        self.x = 0
        self.y = 0

        # Direction of ball in degrees
        self.direction = 0

        # Height and width of the ball
        self.width = 10
        self.height = 10

        # Set the initial ball speed and position
        self.reset("R")

        self.p1_score = 0
        self.p2_score = 0

    def reset(self, winner):
        self.x = 400
        self.y = 350.0
        self.speed=16.0

        # Direction of ball (in degrees)
        if winner == "R":
            self.direction = -45
        else:
            self.direction = 45


    def wall_bounce(self):
        self.direction = (180-self.direction)%360

        # Speed the ball up
        self.speed *= 1.01


    def player_bounce(self, player, diff):
        if player.side == "R":
            self.x = player.x - 20
        elif player.side == "L":
            self.x = player.x + 20
        self.direction = (360-self.direction)%360
        self.direction -= diff

        # Speed the ball up
        self.speed *= 1.01


    # Update the position of the ball
    def update(self):
        # Sine and Cosine work in degrees, so we have to convert them
        direction_radians = math.radians(self.direction)

        # Change the position (x and y) according to the speed and direction
        self.x += self.speed * math.sin(direction_radians)
        self.y -= self.speed * math.cos(direction_radians)

        if self.y < 0:
            self.wall_bounce()

        if self.y > 600:
            self.wall_bounce()

        # Move the image to where our x and y are
        self.rect.x = self.x
        self.rect.y = self.y

        # Do we bounce off the left of the screen?
        if self.x <= 0:
            self.p2_score += 1
            self.reset("L")

        # Do we bounce of the right side of the screen?
        if self.x > self.screenwidth-self.width:
            self.p1_score += 1
            self.reset("R")
