import pygame
import random
from defs import *


class Bird:
    """ Object to store the information of bird movements
    """

    def __init__(self, gameDisplay):
        """ Initialize the bird movement class

        :param gameDisplay: pygame window size
        """

        # Set the display width and height
        self.gameDisplay = gameDisplay

        # Set the bird on living
        self.state = BIRD_ALIVE

        # Load the image of the bird
        self.img = pygame.image.load(BIRD_FILENAME)

        # Get the position of the bird image
        self.rect = self.img.get_rect()

        # Set the start speed at 0
        self.speed = 0

        # Set the start living time at 0 (This is for the AI to see if it works well)
        self.time_lived = 0

        # Set the startpositiom of the bird
        self.set_position(BIRD_START_X, BIRD_START_Y)

    def set_position(self, x, y):
        """ Function to get the initially position of the bird

        :param x: integer, x-position of the bird
        :param y: integer, y-positiion of the bird
        """
        self.rect.centerx = x
        self.rect.centery = y

    def move(self, dt):
        """  Function to update the bird movement variables

        :param dt: integer, time movement in milliseconds
        """

        # When moving, restart the distance and speed
        distance = 0
        new_speed = 0

        # Calculate the distance with s = ut + 0.5at^2
        distance = (self.speed * dt) + (0.5 * GRAVITY * dt * dt)

        # Calculate the speed with v = u + at
        new_speed = self.speed + (GRAVITY * dt)

        # Set the position of the bird on the y axis
        self.rect.centery += distance

        # Set speed of the bird
        self.speed = new_speed

        # If the bird goes above the screen
        if self.rect.top < 0:
            # Let the bird stay in screen
            self.rect.top = 0
            # Set the speed to 0
            self.speed = 0

    def jump(self):
        """ Function to decide if the bird should flap or not
        """

        # If jump is used, reset the speed
        self.speed = BIRD_START_SPEED

    def draw(self):
        """ Function to visualize the bird
        """

        # Draw every frame
        self.gameDisplay.blit(self.img, self.rect)

    def check_status(self, pipes):
        """ Function to check if the bird is still alive

        :param pipes: list, containing pipe information
        """

        # If the bird is below the screen
        if self.rect.bottom > DISPLAY_H:
            # Set the bird status as dead
            self.state = BIRD_DEAD
        # If the bird is still at the screen
        else:
            # Check if the bird hit a pipe
            self.check_hits(pipes)

    def check_hits(self, pipes):
        """ Function to check if the bird hits a pipe

        :param pipes: list, containing pipe information
        """

        # For every pipe in the list
        for p in pipes:
            # When the bird collides with a pipe
            if p.rect.colliderect(self.rect):
                # Set the bird status as dead and stop the loop
                self.state = BIRD_DEAD
                break

    def update(self, dt, pipes):
        """ Function to update the position of a living bird

        :param dt: integer, time movement in milliseconds
        :param pipes: list, containing pipe information
        """

        # Check if the bird is living
        if self.state == BIRD_ALIVE:
            # Update the living time of the bird
            self.time_lived += dt
            # Update the position of the bird
            self.move(dt)
            # Draw the bird at the new position
            self.draw()
            # Check if the bird hits a pipe with the new position
            self.check_status(pipes)
