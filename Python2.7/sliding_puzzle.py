#!/usr/bin/env python

import pygame, sys, random
from pygame.locals import *

# Create some constants
BOARDWIDTH = 6
BOARDHEIGHT = 6
TILESIZE = 100
WINDOWWIDTH = 1024
WINDOWHEIGHT = 768
FPS = 30
BLANK = None

BLACK = (0, 0, 0)
WHITE = (255,255,255)
BRIGHTBLUE = (0,50,255)
DARKTURQUOISE = (3, 54, 73)
GREEN = (0,204,0)

BGCOLOUR = DARKTURQUOISE
TILECOLOUR = GREEN
TEXTCOLOUR = WHITE
BORDERCOLOUR = BRIGHTBLUE
BASICFONTSIZE = 22

BUTTONCOLOUR = WHITE
BUTTONTEXTCOLOUR = BLACK
MESSAGECOLOUR = WHITE

XMARGIN = int((WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)
YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)

UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"


def main():
    global FPSCLOCK, DISPLAY_SURFACE, BASICFONT, RESET_SURFACE, RESET_RECT, NEW_SURFACE, NEW_RECT, SOLVE_SURFACE, SOLVE_RECT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAY_SURFACE = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption("Sliding Game")
    BASICFONT = pygame.font.Font("freesansbold.ttf", BASICFONTSIZE)

    # Store the option buttons and their rectangles in OPTIONS constant.
    RESET_SURFACE, RESET_RECT = makeText("Reset", TEXTCOLOUR, TILECOLOUR, WINDOWWIDTH - 120, WINDOWHEIGHT - 90)
    
