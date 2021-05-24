#!/usr/bin/env python

import pygame
import random
from defs import *  # import properties from defs.py


class Pipe:
    """ Object to store the information of pipe movements
    """

    def __init__(self, gameDisplay, x, y, pipe_type):
        """ Initialize the pipe movement class

        :param gameDisplay: pygame window size
        :param x: integer, x-position of the pipe
        :param y: integer, y-positiion of the pipe
        :param pipe_type: integer, 0 or 1 referring to the lower or upper pipe respectively
        """

        # Set the display width and height
        self.gameDisplay = gameDisplay

        # Set the pipe status to moving
        self.state = PIPE_MOVING

        # Set the pipe type of upper or lower
        self.pipe_type = pipe_type

        # Get the pipe image
        self.img = pygame.image.load(PIPE_FILENAME)

        # Set the location of the pipe image
        self.rect = self.img.get_rect()

        # Set the y-position of the top of the upper pipe
        if pipe_type == PIPE_UPPER:
            y = y - self.rect.height

        # Set the position of the pipe
        self.set_position(x, y)

    def set_position(self, x, y):
        """ Function to get the initially position of the pipe

        :param x: integer, x-position of the pipe
        :param y: integer, y-positiion of the pipe
        """

        # Set the x-position of the pipe
        self.rect.left = x

        # Set the y-position of the pipe
        self.rect.top = y

    def move_position(self, dx, dy):
        """ Function to get new positions of the pipes when moving

        :param dx: integer, number to move the pipe in horizontal direction (x-position)
        :param dy: integer, number to move the pipe in vertical direction (y-position)
        """

        # Update the x-position of the pipe
        self.rect.centerx += dx

        # Update the y-position of the pipe
        self.rect.centery += dy

    def draw(self):
        """ Function to visualize the pipes
        """

        # Set the pipe image at the defined position
        self.gameDisplay.blit(self.img, self.rect)

    def check_status(self):
        """" Function to check the status of the pipe in movement
        """

        # Check if the pipe has left the screen
        if self.rect.right < 0:
            # Update the pipe status from moving to done
            self.state = PIPE_DONE

    def update(self, dt):
        """ Function to update the pipe movement variables

        :param dt: integer, time movement in milliseconds
        """

        # Check if the pipe is moving
        if self.state == PIPE_MOVING:
            # Get the new pipe position
            self.move_position(-(PIPE_SPEED * dt), 0)
            # Visualize the new pipe position
            self.draw()
            # Get the pipe status of moving or done moving
            self.check_status()


class PipeCollection():
    """ Object to store information of new pipes
    """

    def __init__(self, gameDisplay):
        """ Initialize the pipe collection class

        :param gameDisplay: pygame window size
        """

        # Set the display width and height
        self.gameDisplay = gameDisplay
        # Store created pipes
        self.pipes = [] #list of pipes

    def add_new_pipe_pair(self, x): #Add a new pair (UPPER and LOWER) of pipes
        top_y = random.randint(PIPE_MIN, PIPE_MAX - PIPE_GAP_SIZE) #Choose a random position between the boundaries and define the position for the upper pipe
        bottom_y = top_y + PIPE_GAP_SIZE #define position lower pipe

        p1 = Pipe(self.gameDisplay, x, top_y, PIPE_UPPER) #Tie the properties of the pipes together
        p2 = Pipe(self.gameDisplay, x, bottom_y, PIPE_LOWER)

        self.pipes.append(p1) #Create the new pipes
        self.pipes.append(p2)

    def create_new_set(self): #Only called in every new game
        self.pipes = [] #clear the pipe list
        placed = PIPE_FIRST

        while placed < DISPLAY_W: #As long as there is room left on the right
            self.add_new_pipe_pair(placed) #add new pipes
            placed += PIPE_ADD_GAP #and look for the position more to the right

    def update(self, dt):
        rightmost = 0

        for p in self.pipes: #for every pipe in the list
            p.update(dt)
            if p.pipe_type == PIPE_UPPER: #only look at the upper pipe
                if p.rect.left > rightmost: #look for the most right pipe
                    rightmost = p.rect.left #The position of the pipe is the left side of the image

        if rightmost < (DISPLAY_W - PIPE_ADD_GAP): #If the most right pair of pipes had enough room to its right
            self.add_new_pipe_pair(DISPLAY_W) #spawn new pipes

        self.pipes = [p for p in self.pipes if p.state == PIPE_MOVING] #remove pipe pairs that are not moving