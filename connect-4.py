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

### THIS IS A CRAZY NEW COMMENT
#each array is a column with 8 row values --- 8 columns total
board = [
          [ '', '', '', '', '', '', '', ''],
          [ '', '', '', '', '', '', '', ''],
          [ '', '', '', '', '', '', '', ''],
          [ '', '', '', '', '', '', '', ''],
          [ '', '', '', '', '', '', '', ''],
          [ '', '', '', '', '', '', '', ''],
          [ '', '', '', '', '', '', '', ''],
          [ '', '', '', '', '', '', '', '']
]

RED = [255,0,0]
BLUE = [0,0,255]


def play() :
    global board
    player = RED
    gameWon = False
    gameTied = False
    while not gameWon and not gameTied:
        ### get a move from a player -- a column in which to drop a chip
        selectedColumn = getMove(player)
        ### drop the chip -- noting the row of where it ended up
        lastDrop = dropChip(selectedColumn, player)

        # based on the position just dropped into -- see if the player won
        gameWon = checkWin(player, selectedColumn, lastDrop)
        if gameWon:            
            sense.clear()
            if player==RED:
                sense.show_message("Red WINS!", text_colour=player)
            else:
                sense.show_message("Blue WINS!", text_colour=player)
            return

        # if it wasn't a win -- make sure there are still moves that can be made
        gameTied = checkNoMoreMoves()
        if gameTied:
            sense.clear()
            sense.show_message("TIED!!!", 0, 255, 0)
            return

        # if no win and we can still take moves, switch the player and go again!
        if player == RED:
            player = BLUE
        else:
            player = RED        

###------------------------------------------------------
### checkWin does what it sounds like  :)
###------------------------------------------------------    
def checkWin(p, c, r):
    global board
    ### check horizontal    
    leftCount = countAdjacent(p, c, r, 0, -1)
    rightCount = countAdjacent(p, c, r, 0, 1)
    totalCount = 1 + leftCount + rightCount

    if totalCount >= 4:
        return True

    ### check top left to bottom right
    leftCount = countAdjacent(p, c, r, -1, -1)
    rightCount = countAdjacent(p, c, r, 1, 1)
    totalCount = 1 + leftCount + rightCount

    if totalCount >= 4:
        return True

    ### check for bottom left to top right
    leftCount = countAdjacent(p, c, r, 1, -1)
    rightCount = countAdjacent(p, c, r, -1, 1)
    totalCount = 1 + leftCount + rightCount

    if totalCount >= 4:
        return True

    ### check verticle
    downCount = countAdjacent(p, c, r, 1, 0)
    totalCount = 1 + downCount

    if totalCount >= 4:
        return True

    return False

###------------------------------------------------------
### countAdjacent takes a column change (yChange)
###   and rowChange (xChange) and returns the number  
###   of adjacent chips in that direction from the original spot
###------------------------------------------------------    
def countAdjacent(p, c, r, yChange, xChange):
    global board
    adjacentCount = 0
    while True :
        c = c + xChange
        if c < 0 or c > 7:
            return adjacentCount
        
        r = r + yChange
        if r < 0 or r > 7:
            return adjacentCount
        
        if board[c][r] == p:
            adjacentCount = adjacentCount + 1
        else:
            return adjacentCount

###------------------------------------------------------
### checkNoMoreMoves will let you know if there aren't 
###   any more spots to occupy
###------------------------------------------------------    
def checkNoMoreMoves():
    return False

###------------------------------------------------------
### dropChip takes a player (color) and column and
###   "drops" the color as far as it can go and updates
###   the board, returning the y position of the drop
###------------------------------------------------------    
def dropChip(col, p):
    global board
    i=0
        
    while board[col][i] == '':
        if i == 7 or board[col][i+1] != '':
            board[col][i] = p
            return i
        
        sense.set_pixel(col, i, 0,0,0)
        i += 1
        sense.set_pixel(col, i, p[0], p[1], p[2])
        time.sleep(0.1)
        
###------------------------------------------------------
### getMove takes a player (color) and receives input
###   to determine which column it will drop the chip into
###------------------------------------------------------    
def getMove(p) :
    currentColumn = getNextUnoccupiedColumn(-1, 1)
    sense.set_pixel(currentColumn,0, p[0], p[1], p[2]) 

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if currentColumn < 7:
                        if currentColumn >= 0:
                            sense.set_pixel(currentColumn, 0, 0,0,0)                        
                        currentColumn = getNextUnoccupiedColumn(currentColumn, 1)
                        if currentColumn <= 7:
                            sense.set_pixel(currentColumn, 0, p[0], p[1], p[2])
                if event.key == pygame.K_LEFT:
                    if currentColumn > 0:
                        if currentColumn <= 7:
                            sense.set_pixel(currentColumn, 0, 0,0,0)
                        currentColumn = getNextUnoccupiedColumn(currentColumn, -1)
                        if currentColumn >= 0:
                            sense.set_pixel(currentColumn, 0, p[0], p[1], p[2])

                if event.key == pygame.K_RETURN:
                        running = False
                        return currentColumn
                    
###------------------------------------------------------------------
### this will determine the next column (in the first row) that
###   is still unoccupied
###------------------------------------------------------------------                     
def getNextUnoccupiedColumn(currCol, xChange):
    global board
    currCol = currCol + xChange
    while currCol >= 0 and currCol < 7:
        if board[currCol][0] == '':
            return currCol
        currCol = currCol + xChange
    if currCol == 7 and board[currCol][0] != '':
        return 8    
    if currCol == 0 and board[currCol][0] != '':
        return -1
    else:
        return currCol
    
    
###------------------------------------------------------------------
### End of functions
###------------------------------------------------------------------                    
if __name__ == '__main__':
    play()


