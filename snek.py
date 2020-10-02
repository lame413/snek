#!/usr/bin/env python3
import pygame
from enum import Enum
from random import random, randint

pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
teal = (150, 255, 250)

pixelSize = 20
boardSize = 20

display_width = pixelSize * boardSize
display_height = pixelSize * boardSize

gameDisplay = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()

fps = 10

startSnakeLength = 4


class Directions(Enum):
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3


class snakeBlock:
    posX = 0
    posY = 0
    timeToLive = None

    def __init__(self, ttl, x, y):
        self.timeToLive = ttl
        self.posX = x
        self.posY = y

    def updateBlock(self):
        self.timeToLive -= 1


class snakeHead(snakeBlock):
    snakeSegments = []

    direction = Directions.RIGHT
    length = startSnakeLength - 1

    def __init__(self, x, y):
        self.posX = x
        self.posY = y

    def createSegment(self, gb):
        self.snakeSegments.append(snakeBlock(self.length, self.posX, self.posY))


class gameBoard:
    startPos = (int(boardSize / 2), int(boardSize / 2))
    snakeHead = None
    applePos = None

    def spawnSnake(self):
        self.snakeHead = snakeHead(self.startPos[0], self.startPos[1])
        self.snakeHead.createSegment(gameBoard)
        return self.snakeHead

    # Spawns an apple only if it doesn't overlap with the snake
    def createApple(self):
        while self.applePos == None:
            spawnedWell = True
            tmpPos = (randint(0, boardSize - 1), randint(0, boardSize - 1))

            for seg in self.snakeHead.snakeSegments:
                if (seg.posX, seg.posY) == tmpPos:
                    spawnedWell = False
                    break

            if spawnedWell:
                self.applePos = tmpPos

    def game_end(self):
        pygame.display.update()
        gameDisplay.fill((128, 60, 60))
        clock.tick(1)
        for seg in self.snakeHead.snakeSegments[::-1]:
            pygame.draw.rect(
                gameDisplay,
                white,
                (
                    seg.posX * pixelSize + 2,
                    seg.posY * pixelSize + 2,
                    pixelSize - 4,
                    pixelSize - 4,
                ),
            )
            pygame.display.update()

        for seg in self.snakeHead.snakeSegments[::-1]:
            clock.tick(12)
            pygame.draw.rect(
                gameDisplay,
                red,
                (
                    seg.posX * pixelSize + 2,
                    seg.posY * pixelSize + 2,
                    pixelSize - 4,
                    pixelSize - 4,
                ),
            )
            pygame.display.update()

        clock.tick(2)


gameboard = gameBoard()
snake = gameboard.spawnSnake()

crashed = False
alive = True

while not crashed and alive:
    clock.tick(fps)
    prev_dir = snake.direction
    new_dir = prev_dir

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                crashed = True

            if event.key == pygame.K_LEFT and prev_dir != Directions.RIGHT:
                new_dir = Directions.LEFT
            elif event.key == pygame.K_UP and prev_dir != Directions.DOWN:
                new_dir = Directions.UP
            elif event.key == pygame.K_RIGHT and prev_dir != Directions.LEFT:
                new_dir = Directions.RIGHT
            elif event.key == pygame.K_DOWN and prev_dir != Directions.UP:
                new_dir = Directions.DOWN

    # setting new snake direction
    if (
        # are new and old direction opposites?
        (snake.direction.value + 2) % 4 != new_dir.value
        # are new and old directions actually different?
        and new_dir != prev_dir
    ):
        snake.direction = new_dir

    # move the snake
    if snake.direction == Directions.LEFT:
        if snake.posX == 0:
            snake.posX = boardSize - 1
        else:
            snake.posX -= 1
    if snake.direction == Directions.UP:
        if snake.posY == 0:
            snake.posY = boardSize - 1
        else:
            snake.posY -= 1
    if snake.direction == Directions.RIGHT:
        if snake.posX == boardSize - 1:
            snake.posX = 0
        else:
            snake.posX += 1
    if snake.direction == Directions.DOWN:
        if snake.posY == boardSize - 1:
            snake.posY = 0
        else:
            snake.posY += 1

    # Spawn apple if there is none
    if gameboard.applePos == None:
        gameboard.createApple()

    # check if the snake's head is overlapping an apple, if so, set a flag,
    # reset apple and increase snale length
    ateApple = False
    if snake.posX == gameboard.applePos[0] and snake.posY == gameboard.applePos[1]:
        ateApple = True
        gameboard.applePos = None
        snake.length += 1

    # update lifespan of snake segments and remove dead ones
    segments_to_remove = []

    for seg in snake.snakeSegments:
        if not ateApple:
            if seg.timeToLive <= 0:
                segments_to_remove.append(seg)
            seg.updateBlock()

    for s in segments_to_remove:
        snake.snakeSegments.remove(s)

    # collision detection with snake body
    for seg in snake.snakeSegments:
        if snake.posX == seg.posX and snake.posY == seg.posY:
            gameboard.game_end()
            crashed = True

    snake.createSegment(gameboard)

    # update the display
    gameDisplay.fill(black)

    # display apple if present
    if not ateApple:
        pygame.draw.rect(
            gameDisplay,
            red,
            (
                gameboard.applePos[0] * pixelSize + 4,
                gameboard.applePos[1] * pixelSize + 4,
                pixelSize - 8,
                pixelSize - 8,
            ),
        )

    # draw snake segments
    for seg in snake.snakeSegments:
        if seg.posX == snake.posX and seg.posY == snake.posY:
            pygame.draw.rect(
                gameDisplay,
                teal,
                (
                    seg.posX * pixelSize + 2,
                    seg.posY * pixelSize + 2,
                    pixelSize - 4,
                    pixelSize - 4,
                ),
            )
        else:
            pygame.draw.rect(
                gameDisplay,
                white,
                (
                    seg.posX * pixelSize + int(pixelSize / 10),
                    seg.posY * pixelSize + int(pixelSize / 10),
                    pixelSize - int(pixelSize / 5),
                    pixelSize - int(pixelSize / 5),
                ),
            )

    pygame.display.update()

    # score - 'snake.length' doesn't count the head
    if snake.length >= 10:
        pygame.display.set_caption("snek - " + str(snake.length + 1))
    else:
        pygame.display.set_caption(snake.length * "s" + "snek")

    # if snake fills etire board - quit/win
    if snake.length >= (boardSize * boardSize) - 1:
        crashed = True


pygame.quit()
