#!/usr/bin/env python

import random, pygame, sys
from pygame.locals import *

FPS = 30
WINWIDTH = 640
WINHEIGHT = 480
REVEALSPEED = 8 # in seconds
BOXSIZE = 40
GAPSIZE = 10
COLUMNS = 10
ROWS = 7
assert (COLUMNS * ROWS) % 2 == 0, "Board needs to have an even number of boxes for pairs"
XMARGIN = int((WINWIDTH - (COLUMNS * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINHEIGHT - (ROWS * (BOXSIZE + GAPSIZE))) / 2)

GREY = (100, 100, 100)
NAVY = ( 60, 60, 80)
WHITE = (244, 244, 244)
RED = (200, 0, 0)
GREEN = ( 0, 230, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (205, 0, 205)
CYAN = (0, 240, 240)

BGCOLOR = NAVY
LIGHTBGCOLOR = GREY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

DONUT = "donut"
SQUARE = "square"
DIAMOND = "diamond"
LINES = "lines"
OVAL = "oval"

ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)
assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= COLUMNS * ROWS, "Board is too big for colours, shapes"

def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))

    mousex = 0 
    mousey = 0
    pygame.display.set_caption("Memory Game")
    mainBoard = getRandomizedBoard()
    revealedBoxes = genRevealedBoxesData(False)
    firstSelection = None # stores the x and y of the first box clicked
    DISPLAYSURF.fill(BGCOLOR)
    startGameAnimation(mainBoard)

    while True: # main game loop
        mouseClicked = False
        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(mainBoard, revealedBoxes)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
            boxX, boxY = getBoxAtPixel(mousex, mousey)
            if boxX != None and boxY != None:
                # mouse over a box
                if not revealedBoxes[boxX][boxY]:
                    drawHighlightBox(boxX, boxY)
                if not revealedBoxes[boxX][boxY] and mouseClicked:
                    revealBoxesAnimation(mainBoard, [(boxX, boxY)])
                    revealedBoxes[boxX][boxY] = True # set the box to 'revealed'
                    if firstSelection == None:
                        firstSelection = (boxX, boxY)
                    else:
                        # current box was 2nd box clicked, check for a match
                        icon1shape, icon1color = getShapeColour(mainBoard, firstSelection[0], firstSelection[1])
                        icon2shape, icon2color = getShapeColour(mainBoard, boxX, boxY)
                        if icon1shape != icon2shape or icon1color != icon2color:
                            # no match, re-cover selections
                            pygame.time.wait(1000) # ms
                            coverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (boxX, boxY)])
                            revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                            revealedBoxes[boxX][boxY] = False
                        elif hasWon(revealedBoxes): # check if all pairs found
                            gameWonAnimation(mainBoard)
                            pygame.time.wait(2000)
                            # reset the board
                            mainBoard = getRandomizedBoard()
                            revealedBoxes = genRevealedBoxesData(False)
                            # replay start game animation
                            startGameAnimation(mainBoard)
                        firstSelection = None

        # redraw the screen and wait a clock tick.
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def genRevealedBoxesData(val):
    revealedBoxes = []
    for i in range(COLUMNS):
        revealedBoxes.append([val] * ROWS)
    return revealedBoxes


def getRandomizedBoard():
    # get a list of every permutation of icons
    icons = []
    for color in ALLCOLORS:
        for shape in ALLSHAPES:
            icons.append( (shape, color) )
    random.shuffle(icons)
    numIconsUsed = int(COLUMNS * ROWS / 2 )
    icons = icons[:numIconsUsed] * 2 # make two of each icon
    random.shuffle(icons)

    # Create the board data structure, with randomly placed icons.
    board = []
    for x in range(COLUMNS):
        column = []
        for y in range(ROWS):
            column.append(icons[0])
            del icons[0] # remove the icons as we assign them
        board.append(column)
    return board


def splitIntoGroupsOf(groupSize, theList):
    result = []
    for i in range(0, len(theList), groupSize):
        result.append(theList[i:i + groupSize])
    return result


def leftTopCoordsOfBox(boxX, boxY):
    # Convert board coordinates to pixel coordinates
    left = boxX * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxY * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)


def getBoxAtPixel(x, y):
    for boxX in range(COLUMNS):
        for boxY in range(ROWS):
            left, top =leftTopCoordsOfBox(boxX, boxY)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxX, boxY)
    return (None, None)


def drawIcon(shape, color, boxX, boxY):
    quarter = int(BOXSIZE * 0.25)
    half = int(BOXSIZE * 0.5)

    left, top = leftTopCoordsOfBox(boxX, boxY) # get pixel coords from board coords
    # draw some shapes
    if shape == DONUT:
        pygame.draw.circle(DISPLAYSURF, color, (left + half, top + half), half - 5)
        pygame.draw.circle(DISPLAYSURF, BGCOLOR, (left + half, top + half), quarter - 5)
    elif shape == SQUARE:
        pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top + quarter, BOXSIZE - half, BOXSIZE - half))
    elif shape == DIAMOND:
        pygame.draw.polygon(DISPLAYSURF, color, ((left + half, top), (left + BOXSIZE -1, top + half), (left + half, top + BOXSIZE - 1), (left, top + half)))
    elif shape == LINES:
        for i in range(0, BOXSIZE, 4):
            pygame.draw.line(DISPLAYSURF, color, (left, top + i), (left + i, top))
            pygame.draw.line(DISPLAYSURF, color, (left + i, top + BOXSIZE -1), (left + BOXSIZE -1, top + i))
    elif shape == OVAL:
        pygame.draw.ellipse(DISPLAYSURF, color, (left, top + quarter, BOXSIZE, half))


def getShapeColour(board, boxX, boxY):
    # shape value for x, y spot is stored in board[x][y][0]
    return board[boxX][boxY][0], board[boxX][boxY][1]


def drawBoxCovers(board, boxes, coverage):
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))
        shape, color = getShapeColour(board, box[0], box[1])
        drawIcon(shape, color, box[0], box[1])
        if coverage > 0:  
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, coverage, BOXSIZE))
    pygame.display.update()
    FPSCLOCK.tick(FPS)


def revealBoxesAnimation(board, boxesToReveal):
    # Reveal a symbol
    for coverage in range(BOXSIZE, (-REVEALSPEED) - 1, - REVEALSPEED):
        drawBoxCovers(board, boxesToReveal, coverage)


def coverBoxesAnimation(board, boxesToCover):
    # cover an icon
    for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
        drawBoxCovers(board, boxesToCover, coverage)


def drawBoard(board, revealed):
    # Draws all of the boxes in their covered or revealed state.
    for boxX in range(COLUMNS):
        for boxY in range(ROWS):
            left, top = leftTopCoordsOfBox(boxX, boxY)
            if not revealed[boxX][boxY]:
                # draw covered box
                pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            else:
                # a revealed icon
                shape, color = getShapeColour(board, boxX, boxY)
                drawIcon(shape, color, boxX, boxY)


def drawHighlightBox(boxX, boxY):
    left, top = leftTopCoordsOfBox(boxX, boxY)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left - 5, top - 5, BOXSIZE + 10, BOXSIZE +10), 4)


def startGameAnimation(board):
    # randomly reveal some boxes
    coveredBoxes = genRevealedBoxesData(False)
    boxes = []
    for x in range(COLUMNS):
        for y in range(ROWS):
            boxes.append( (x, y) )
    random.shuffle(boxes)
    boxGroups = splitIntoGroupsOf(8, boxes)

    drawBoard(board, coveredBoxes)
    for boxGroup in boxGroups:
        revealBoxesAnimation(board, boxGroup)
        coverBoxesAnimation(board, boxGroup)


def gameWonAnimation(board):
    # flash the bg colour when the player has won
    coveredBoxes = genRevealedBoxesData(True)
    color1 = LIGHTBGCOLOR
    color2 = BGCOLOR

    for i in range(13):
        color1, color2 = color2, color1
        DISPLAYSURF.fill(color1)
        drawBoard(board, coveredBoxes)
        pygame.display.update()
        pygame.time.wait(300)


def hasWon(revealedBoxes):
    # True if all boxes revealed
    for i in revealedBoxes:
        if False in i:
            return False # false if any boxes covered
    return True


if __name__ == '__main__':
    main()
