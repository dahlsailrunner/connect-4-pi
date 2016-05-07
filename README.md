# connect-4-pi
Connect-4 for the Raspberry Pi with a Sense HAT

A full discussion of this code and how it got started is located on my blog here.  Basically this is an implementation of the classic game of Connect-4 using the 8x8 LED matrix of the Pi Sense HAT with a Raspberry Pi 2.

# Getting Started #
The two python files here are the iterative variants of me and some Makers Club members from a school working our way to a functional Connect-4 game.

We started by expanding the example code that is available from the Sense HAT, which showed usage of the joystick, and individual pixel control for the LED matrix.

##  connect-4-getting-started.py ##
This program simply gets a move by lighting up the top left pixel, letting the player move it left and right using the joystick, and then dropping the "chip" when the push the joystick in.  It then changes color and repeats the same.  No provision for keeping track of what board spots are occupied is built in this code -- it's very simple.

## connect-4.py ##
This is the mostly-complete full implementation of the game.  The only thing still missing (and it would be easy to add) is the correct checking to see if all of the board spots are occupied, thus triggering a tie game.