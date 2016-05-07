#!/usr/bin/env python
from sense_hat import SenseHat
import os
import time
import pygame  # See http://www.pygame.org/docs
from pygame.locals import *

#### ---------------------------------------------
####  Just some stuff to get started
#### ---------------------------------------------
pygame.init()
pygame.display.set_mode((640, 480))

sense = SenseHat()
sense.clear()  # Blank the LED matrix

RED = [255,0,0]
BLUE = [0,0,255]


def play() :
    player = RED
    
    while True:
        ### get a move from a player -- a column in which to drop a chip
        selectedColumn = getMove(player)
        ### drop the chip 
        dropChip(selectedColumn, player)
        
        if player == RED:
            player = BLUE
        else:
            player = RED        


###------------------------------------------------------
### dropChip takes a player (color) and column and
###   "drops" the color as far as it can go and updates
###   the board, returning the y position of the drop
###------------------------------------------------------    
def dropChip(col, p): 
    i=0
        
    while i < 7:
        sense.set_pixel(col, i, 0,0,0)
        i += 1
        sense.set_pixel(col, i, p[0], p[1], p[2])
        time.sleep(0.1)
        
###------------------------------------------------------
### getMove takes a player (color) and receives input
###   to determine which column it will drop the chip into
###------------------------------------------------------    
def getMove(p) :
    currentColumn = 0
    sense.set_pixel(currentColumn,0, p[0], p[1], p[2]) 

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if currentColumn < 7:                       
                        sense.set_pixel(currentColumn, 0, 0,0,0)                        
                        currentColumn += 1                        
                        sense.set_pixel(currentColumn, 0, p[0], p[1], p[2])
                if event.key == pygame.K_LEFT:
                    if currentColumn > 0:                        
                        sense.set_pixel(currentColumn, 0, 0,0,0)
                        currentColumn -= 1                         
                        sense.set_pixel(currentColumn, 0, p[0], p[1], p[2])

                if event.key == pygame.K_RETURN:
                        running = False
                        return currentColumn
                        
    
###------------------------------------------------------------------
### End of functions
###------------------------------------------------------------------                    
if __name__ == '__main__':
    play()


