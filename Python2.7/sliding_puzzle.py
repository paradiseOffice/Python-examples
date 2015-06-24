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
    NEW_SURFACE, NEW_RECT = makeText("New Game", TEXTCOLOUR, TILECOLOUR, WINDOWWIDTH - 120, WINDOWHEIGHT - 60)
    SOLVE_SURFACE, SOLVE_RECT = makeText("Solve", TEXTCOLOUR, TILECOLOUR, WINDOWWIDTH - 120, WINDOWHEIGHT - 30)
    mainBoard, solutionSeq = generateNewPuzzle(80)
    SOLVEDBOARD = getStartingBoard() # The board in its start state
    allMoves = [] # moves made from the solved configuration

    while True: # main game loop 
        slideTo = None # the direction in which the tile should slide, if any
        msg = ""  # msg for upper left corner
        if mainBoard == SOLVEDBOARD:
            msg = "Solved!"

        drawBoard(mainBoard, msg)

        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                spotx, spoty = getSpotClicked(mainBoard, event.pos[0], event.pos[1])
                if (spotx, spoty) == (None, None):
                    # check if the user clicked on an option button
                    if RESET_RECT.collidepoint(event.pos):
                        resetAnimation(mainBoard, allMoves)
                        allMoves = []
                    elif NEW_RECT.collidepoint(event.pos):
                        mainBoard, solutionSeq = generateNewPuzzle(80)
                        allMoves = []
                    elif SOLVE_RECT.collidepoint(event.pos):
                        resetAnimation(mainBoard, solutionSeq + allMoves)
                        allMoves = []
                    else:
                        # check if the clicked tile was next to the blank spot
                        blankx, blanky = getBlankPosition(mainBoard)
                        if spotx == blankx + 1 and spoty == blanky:
                            slideTo = LEFT
                        elif spotx == blankx - 1 and spoty == blanky:
                            slideTo = RIGHT
                        elif spotx == blankx and spoty == blanky + 1:
                            slideTo = UP
                        elif spotx == blankx and spoty == blanky - 1:
                            slideTo = DOWN
                    elif event.type == KEYUP:
                        # for cursor keys
                        if event.key in (K_LEFT, K_a) and isValidMove(mainBoard, LEFT):
                            slideTo = LEFT
                        elif event.key in (K_RIGHT, K_d) and isValidMove(mainBoard, RIGHT):
                            slideTo = RIGHT
                        elif event.key in (K_UP, K_w) and isValidMove(mainBoard, UP):
                            slideTo = UP
                        elif event.key in (K_DOWN, K_s) and isValidMove(mainBoard, DOWN):
                            slideTo = DOWN
        if slideTo:
            slideAnimation(mainBoard, slideTo, "Click tile or use cursor keys to slide.", 8)
            makeMove(mainBoard, slideTo)
            allMoves.append(slideTo) # record the slide
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event) # put the other keyup events back


def getStartingBoard():
    # Return a solved board structure
    # For example, if BOARDWIDTH and BOARDHEIGHT are both 3, this function
    # returns [[1, 4, 7], [2, 5, 8], [3, 6, None]]
    counter = 1
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(counter)
            counter += BOARDWIDTH
        board.append(column)
        counter -= BOARDWIDTH * (BOARDHEIGHT - 1) + BOARDWIDTH - 1

    board[BOARDWIDTH-1][BOARDHEIGHT-1] = None
    return board


def getBlankPosition(board):
    # Return the x and y of board coordinates
