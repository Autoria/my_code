__author__ = 'Liu_100'
#-*- coding:utf-8 -*-
import pygame, sys, random
from pygame.locals import*
FPS = 15
WINDOWWIDTH =640
WINDOWHEIGHT = 480
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size"
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height muset be multiple of cell size"
CELLWIDTH = WINDOWWIDTH / CELLSIZE  #
CELLHEIGHT = WINDOWHEIGHT / CELLSIZE    #

#RGB
WHITE = (255, 255, 255)
BLACK = (0, 0 , 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
DARKGRAY = (40, 40, 40)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 #

#main function
def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('snakey')

    showStartScreen()  #
    while True:
        runGame()   #
        showGameOverScreen()    #

def runGame():
    #
    startx = random.randint(5, CELLWIDTH-6)
    starty = random.randint(5, CELLHEIGHT-6)
    snakeCoods = [{'x': startx, 'y': starty},
                 {'x': startx-1, 'y': starty},
                 {'x': startx-2, 'y': starty}]
    direction = RIGHT   #

    apple = getRandomLocation()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:     #
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT

                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT

                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP

                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN

                elif event.key == K_ESCAPE:
                    terminate()

        if snakeCoods[HEAD]['x'] == -1 or snakeCoods[HEAD]['x'] == CELLWIDTH or snakeCoods[HEAD]['y'] == -1 or snakeCoods[HEAD]['y'] == CELLHEIGHT:
            return #game over
        for snakeBody in snakeCoods[1:]:
            if snakeBody['x'] == snakeCoods[HEAD]['x'] and snakeBody['y'] == snakeCoods[HEAD]['y']:
                return #game over
        #
        if snakeCoods[HEAD]['x'] == apple['x'] and snakeCoods[HEAD]['y'] == apple['y']:
            apple = getRandomLocation() #
        else:
            del snakeCoods[-1] #
        #
        if direction == UP:
            newHead = {'x': snakeCoods[HEAD]['x'], 'y': snakeCoods[HEAD]['y']-1}
        elif direction == DOWN:
            newHead = {'x': snakeCoods[HEAD]['x'], 'y': snakeCoods[HEAD]['y']+1}
        elif direction == LEFT:
            newHead = {'x': snakeCoods[HEAD]['x']-1, 'y': snakeCoods[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': snakeCoods[HEAD]['x']+1, 'y': snakeCoods[HEAD]['y']}
        snakeCoods.insert(0,newHead)
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid() #
        drawsnake(snakeCoods) #
        drawApple(apple) #
        drawScore(len(snakeCoods) - 3)#
        pygame.display.update()
        FPSCLOCK.tick(FPS)



#
def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 20, WINDOWHEIGHT-30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

#
def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()
    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key

#
def showStartScreen():
        titleFont = pygame.font.Font('freesansbold.ttf', 100)
        titleSurf1 = titleFont.render('Hello!', True, WHITE, DARKGREEN)
        titleSurf2 = titleFont.render('snakey!', True, GREEN)

        degrees1 = 0
        degrees2 = 0
        while True:
                DISPLAYSURF.fill(BGCOLOR)
                rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
                rotatedRect1 = rotatedSurf1.get_rect()
                rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
                DISPLAYSURF.blit(rotatedSurf1,rotatedRect1)

                rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
                rotatedRect2 = rotatedSurf2.get_rect()
                rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
                DISPLAYSURF.blit(rotatedSurf2,rotatedRect2)

                drawPressKeyMsg()

                if checkForKeyPress():
                    pygame.event.get()
                    return
                pygame.display.update()
                FPSCLOCK.tick(FPS)
                degrees1 += 3
                degrees2 += 7

#
def terminate():
    pygame.quit()
    sys.exit()

#
def getRandomLocation():
    return  {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}

#
def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('GAME', True, WHITE)
    overSurf = gameOverFont.render('OVER', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress()

    while True:
        if checkForKeyPress():
            pygame.event.get()
            return

def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' %(score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

def drawsnake(snakeCoods):
    for coord in snakeCoods:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        snakeSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, snakeSegmentRect)
        snakeInnerSegmentRect = pygame.Rect(x+4, y+4, CELLSIZE-8, CELLSIZE-8)
        pygame.draw.rect(DISPLAYSURF, GREEN, snakeInnerSegmentRect)

def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)

def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE):
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE):
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))

if __name__ == '__main__':
    main()
