import pygame
import neat
import time
import os
import random

WIN_WIDTH = 600
WIN_HEIGHT = 800

#Makes all the images larger

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load("bird1.png")),pygame.transform.scale2x(pygame.image.load("bird2.png")),pygame.transform.scale2x(pygame.image.load("bird3.png"))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load("pipe.png"))
BASE_IMG = pygame.transform.scale2x(pygame.image.load("base.png"))
BG_IMG = pygame.transform.scale2x(pygame.image.load("background.png"))

class Bird:
    IMGS=BIRD_IMGS
    MAX_ROTATION=25 #Degree of rotation
    ROT_VEL=20 #How fast it rotates
    ANIMATION_TIME = 5 #How fast is the bird animated in terms of how fast it flaps wings
    
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.tilt=0 #The bird is flat i.e 0 degrees initially
        self.tick_count = 0
        self.vel=0 #Velocity of the bird
        self.height = self.y
        self.img_count = 0 #Tracks which image we are showing for the bird
        self.img = self.IMGS[0] #Stores the initial bird image

    def jump(self):
        self.vel = -10.5 #The bird has to jump upwards, top left of pygame window is (0,0) moving to the right increases x and moving down increases y
        self.tick_count=0 #Keeps track of when we last jumped
        self.height = self.y #Keeps track of where the bird jumped from/started moving from
    
    def move(self):
        self.tick_count+=1 #Represents time in the next line
        d=self.vel*self.tick_count + 1.5*self.tick_count**2 #Calculates the displacement upwards using d = ut+0.5*a*t^2, a is 3 since a is positive the acceleration is downwards

        if d>=16: #Dont move down too fast
            d=16 
        
        if d<0: #Finetunes upward movement
            d-=2
        
        self.y = self.y + d #Updating y direction

        if d<0:
            if self.tilt < self.MAX_ROTATION: #Tilt upwards if displacement is upwards
                self.tilt=self.MAX_ROTATION
        else:
            if self.tilt>-90:   #Nosedive in other case
                self.tilt-=self.ROT_VEL







