__author__ = 'Liu_100'
# -*- coding: utf-8 -*-
import pygame
import random
from pygame.locals import *
import sys


FPS = 15
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20

assert WINDOWWIDTH % CELLSIZE == 0, "Width/Cellsize error"
assert WINDOWHEIGHT % CELLSIZE == 0, "Height/Cellsize error"
CELLWIDTH = WINDOWWIDTH/CELLSIZE
CELLHEIGHT = WINDOWHEIGHT/CELLSIZE

#color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
DARKGRAY = (40, 40, 40)
BGCOLOR = BLACK

#operation
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0
#
def main():
    global FPSClock, displaySurface, basicFont

    pygame.init()
    FPSClock = pygame.time.Clock()
    FPS = 15
    displaySurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    basicFont = pygame.font.Font("freesansbold.ttf", 18)
    pygame.display.set_caption("snake")

    showStartScreen()
    showLogScreen()
    while True:
        runGame()
        showGameOver()

def runGame():
    start_x = random.randint(5, CELLWIDTH-6)
    start_y = random.randint(5, CELLHEIGHT-6)
    snakeCoods = [{'x': start_x, 'y': start_y},
                 {'x': start_x-1, 'y': start_y},
                 {'x': start_x-2, 'y': start_y}]
    direction = RIGHT

    apple = getRandomLocation()
    directionList = []
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                    directionList.append(direction)
                    # break
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                    directionList.append(direction)
                    # break
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                    directionList.append(direction)
                    # break
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                    directionList.append(direction)
                    # break
                elif event.key == K_ESCAPE:
                    terminate()
        if directionList:
            direction = directionList[0]
            del directionList[0]
        #GAME OVER EXAM, Collision
        if snakeCoods[HEAD]['x'] == -1 or snakeCoods[HEAD]['x'] == CELLWIDTH or snakeCoods[HEAD]['y'] == -1 or snakeCoods[HEAD]['y'] == CELLHEIGHT:
            return
        for snakeBody in snakeCoods[1:]:
            if snakeBody['x'] == snakeCoods[HEAD]['x'] and snakeBody['y'] == snakeCoods[HEAD]['y']:
                return

        if snakeCoods[HEAD]['x'] == apple['x'] and snakeCoods[HEAD]['y'] == apple['y']:
            apple = getRandomLocation()
        else:
            del snakeCoods[-1] #


        if direction == UP:
            newHead = {'x': snakeCoods[HEAD]['x'], 'y': snakeCoods[HEAD]['y']-1}
        elif direction == DOWN:
            newHead = {'x': snakeCoods[HEAD]['x'], 'y': snakeCoods[HEAD]['y']+1}
        elif direction == LEFT:
            newHead = {'x': snakeCoods[HEAD]['x']-1, 'y': snakeCoods[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': snakeCoods[HEAD]['x']+1, 'y': snakeCoods[HEAD]['y']}
        snakeCoods.insert(0,newHead)
        displaySurface.fill(BGCOLOR)
        drawGrid() #
        drawSnake(snakeCoods) #
        drawApple(apple) #
        drawScore(len(snakeCoods) - 3)#
        pygame.display.update()
        FPSClock.tick(FPS)





def completeNewFrame(direction, snakeCoods, apple):
    if direction == UP:
        newHead = {'x': snakeCoods[HEAD]['x'], 'y': snakeCoods[HEAD]['y'] - 1}
    elif direction == DOWN:
        newHead = {'x': snakeCoods[HEAD]['x'], 'y': snakeCoods[HEAD]['y'] + 1}
    elif direction == LEFT:
        newHead = {'x': snakeCoods[HEAD]['x'] - 1, 'y': snakeCoods[HEAD]['y']}
    elif direction == RIGHT:
        newHead = {'x': snakeCoods[HEAD]['x'] + 1, 'y': snakeCoods[HEAD]['y']}

    snakeCoods.insert(0, newHead)
    displaySurface.fill(BGCOLOR)
    drawGrid()
    drawSnake(snakeCoods)
    drawApple(apple)
    drawScore(len(snakeCoods) - 3)
    pygame.display.update()


def exameKeyPress(direction):
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        elif event.type == KEYDOWN:
            if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                direction = LEFT
                break
            elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                direction = RIGHT
                break
            elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                direction = UP
                break
            elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                direction = DOWN
                break
            elif event.key == K_ESCAPE:
                terminate()
    return direction

def drawPressKeyMsg():
    pressKeySurf = basicFont.render('Press a key to continue.', True, DARKGREEN)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT-30)
    displaySurface.blit(pressKeySurf, pressKeyRect)
#
def checkForQuit():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()
    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf',100)
    titleSurf1 = titleFont.render('Hello!', True, WHITE, DARKGREEN)
    titleSurf2 = titleFont.render('Snake!', True, GREEN)

    degrees1 = 0
    degrees2 = 0
    while True:
        displaySurface.fill(BGCOLOR)

        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)
        displaySurface.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)
        displaySurface.blit(rotatedSurf2,rotatedRect2)

        pygame.display.update()
        drawPressKeyMsg()

        if checkForQuit():
            pygame.event.get()
            return
        pygame.display.update()
        FPSClock.tick(FPS)
        degrees1 += 3
        degrees2 += 7

def showLogScreen():
    displaySurface.fill(BGCOLOR)
    MenuFont = pygame.font.Font('freesansbold.ttf', 40)

    StartSurf = MenuFont.render('Start', True, WHITE)
    RankSurf = MenuFont.render('Rank', True, WHITE)
    SpeedSurf = MenuFont.render('Speed', True, WHITE)
    StartRect = StartSurf.get_rect()
    RankRect = RankSurf.get_rect()
    SpeedRect = SpeedSurf.get_rect()
    StartRect.midtop = (WINDOWWIDTH/2, 160)
    RankRect.midtop = (WINDOWWIDTH/2, StartRect.height+160+25)
    SpeedRect.midtop = (WINDOWWIDTH/2, StartRect.height+160+25+25+RankRect.height)

    displaySurface.blit(StartSurf, StartRect)
    displaySurface.blit(RankSurf, RankRect)
    displaySurface.blit(SpeedSurf, SpeedRect)
    pygame.display.update()
    while True:
        if checkForQuit():
            pygame.event.get()
            return
        if pygame.mouse.get_pressed()[0]:
            if StartRect.collidepoint( pygame.mouse.get_pos() ):
                return
            if RankRect.collidepoint( pygame.mouse.get_pos() ):
                showRankScreen()
                return
            if SpeedRect.collidepoint( pygame.mouse.get_pos() ):
                showSpeedScreen()
                return

def showSpeedScreen():
    displaySurface.fill(BGCOLOR)
    GREEN = (0,255,0)
    HFGREEN = (0,125,0)
    speedRect = pygame.Rect(0, 190, 640, 100)
    while True:

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return

        pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            factor = pos[0]/639.
        global FPS
        FPS = int(factor*60) + 5
        pygame.display.set_caption("Speed-%d"%FPS)
        pygame.draw.rect(displaySurface, GREEN, speedRect)
        pygame.draw.circle(displaySurface, HFGREEN, (int(factor*639.0), 240), 50)
        pygame.display.update()
def showRankScreen():
    displaySurface.fill(BGCOLOR)
    return

def terminate():
    pygame.quit()
    sys.exit()

def getRandomLocation():
    return {'x':random.randint(0,CELLWIDTH-1), 'y':random.randint(0,CELLHEIGHT-1)}

def showGameOver():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render("Game", True, WHITE)
    overSurf = gameOverFont.render("Over", True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH/2, 10)
    overRect.midtop = (WINDOWWIDTH/2, gameRect.height +10 +25)

    displaySurface.blit(gameSurf, gameRect)
    displaySurface.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)

    while True:
        if checkForQuit():
            pygame.event.get()
            return
def drawScore(score):
    scoreSurf = basicFont.render("Score: %s" %(score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH-120, 10)
    displaySurface.blit(scoreSurf, scoreRect)

def drawSnake(snakeCoods):
    for coord in snakeCoods:
        x = coord['x'] * CELLSIZE
        y =coord['y'] * CELLSIZE
        snakeSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(displaySurface, DARKGREEN, snakeSegmentRect)
        snakeInnerSegmentRect = pygame.Rect(x+4, y+4, CELLSIZE-8, CELLSIZE-8)
        pygame.draw.rect(displaySurface, GREEN, snakeInnerSegmentRect)

def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(displaySurface, RED, appleRect)

def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE):
        pygame.draw.line(displaySurface, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE):
        pygame.draw.line(displaySurface, DARKGRAY, (0, y), (WINDOWWIDTH, y))

if __name__ == '__main__':
    main()
