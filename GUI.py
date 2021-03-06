import pygame
import random
import os
import Wampus as w

pygame.init()

WALL_WIDTH = 20
SCREEN_SIZE = 800

SQUARES_NUM = w.world_width
SQUARES_WIDTH = int(SCREEN_SIZE/SQUARES_NUM)

HOLES = []
HOLE_SIZE = 170

BORDERS = []

GOLD = ()
GOLD_SIZE = 170

WUMPUS = ()
WUMPUS_SIZE = 170

DEAD_WUMPUS = ()
DEAD_WUMPUS_SIZE = 170

AGENT = ()
AGENT_SIZE = 170

screen = pygame.display.set_mode([SCREEN_SIZE + 2 * WALL_WIDTH, SCREEN_SIZE + 2 * WALL_WIDTH])
# coin
coins = pygame.image.load('diamond_ore.png').convert()
coins.set_colorkey((255, 255, 255))
scaled_coin = pygame.transform.scale(coins, (GOLD_SIZE, GOLD_SIZE))
colored_scaled_coin = scaled_coin.set_colorkey((255, 255, 255))

# hole
hole = pygame.image.load('hole2.png').convert()
hole.set_colorkey((255, 255, 255))
scaled_hole = pygame.transform.scale(hole, (HOLE_SIZE, HOLE_SIZE))

# creeper
creeper = pygame.image.load('creeper.jpg').convert()
creeper.set_colorkey((255, 255, 255))
scaled_creeper = pygame.transform.scale(creeper, (WUMPUS_SIZE, WUMPUS_SIZE))

# dead creeper
dead_creeper = pygame.image.load('gunpowder.png').convert()
dead_creeper.set_colorkey((255, 255, 255))
scaled_dead_creeper = pygame.transform.scale(dead_creeper, (WUMPUS_SIZE, WUMPUS_SIZE))

# agent(Steve)
steve = pygame.image.load('steeve.png').convert()
steve.set_colorkey((255, 255, 255))
scaled_steve = pygame.transform.scale(steve, (WUMPUS_SIZE, WUMPUS_SIZE))


def initMap(world, dude):
    global AGENT
    AGENT = dude.pos
    for i in range(SQUARES_NUM):
        for j in range(SQUARES_NUM):
            if world[i, j] == 1:
                HOLES.append((i, j))
            if world[i, j] == 3:
                global GOLD
                GOLD = (i, j)
            if world[i, j] == 2:
                global WUMPUS
                WUMPUS = (i, j)
            if world[i, j] == 6:
                global DEAD_WUMPUS
                DEAD_WUMPUS = (i, j)


def drawWorld(outer_world, dude):

    initMap(outer_world, dude)
    # Set up the drawing window

    running = True

    if running:

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the background with white
        screen.fill((0, 0, 10))

        # walls
        pygame.draw.rect(screen, (89, 36, 36), (0, 0, SCREEN_SIZE + WALL_WIDTH, WALL_WIDTH))
        pygame.draw.rect(screen, (89, 36, 36), (0, 0, WALL_WIDTH, SCREEN_SIZE + WALL_WIDTH))
        pygame.draw.rect(screen, (89, 36, 36), (SCREEN_SIZE + WALL_WIDTH, 0, SCREEN_SIZE + WALL_WIDTH,
                                                SCREEN_SIZE + 2 * WALL_WIDTH))
        pygame.draw.rect(screen, (89, 36, 36), (0, SCREEN_SIZE + WALL_WIDTH, SCREEN_SIZE + WALL_WIDTH,
                                                SCREEN_SIZE + 2 * WALL_WIDTH))

        # lines vertical
        for i in range(SQUARES_NUM):
            pygame.draw.line(screen, (89, 36, 36), (WALL_WIDTH + (i + 1) * SQUARES_WIDTH, 0),
                             (WALL_WIDTH + (i + 1) * SQUARES_WIDTH, SCREEN_SIZE + WALL_WIDTH))

        # lines horizontal
        for i in range(SQUARES_NUM):
            pygame.draw.line(screen, (89, 36, 36), (0, WALL_WIDTH + (i + 1) * SQUARES_WIDTH),
                             (SCREEN_SIZE + WALL_WIDTH, WALL_WIDTH + (i + 1) * SQUARES_WIDTH))

        # gold
        screen.blit(scaled_coin, (int(GOLD[1] * SQUARES_WIDTH + WALL_WIDTH + (SQUARES_WIDTH - GOLD_SIZE) / 2),
                                  int(GOLD[0] * SQUARES_WIDTH + WALL_WIDTH + (SQUARES_WIDTH - GOLD_SIZE) / 2)))

        # holes
        for i in HOLES:
            screen.blit(scaled_hole, (int(i[1] * SQUARES_WIDTH + WALL_WIDTH + (SQUARES_WIDTH - HOLE_SIZE) / 2),
                                      int(i[0] * SQUARES_WIDTH + WALL_WIDTH + (SQUARES_WIDTH - HOLE_SIZE) / 2)))

        # creeper
        if 2 in outer_world:
            screen.blit(scaled_creeper, (int(WUMPUS[1] * SQUARES_WIDTH + WALL_WIDTH
                                             + (SQUARES_WIDTH - WUMPUS_SIZE) / 2),
                                         int(WUMPUS[0] * SQUARES_WIDTH + WALL_WIDTH
                                             + (SQUARES_WIDTH - WUMPUS_SIZE) / 2)))

        # dead creeper
        if 6 in outer_world:
            screen.blit(scaled_dead_creeper, (int(DEAD_WUMPUS[1] * SQUARES_WIDTH + WALL_WIDTH +
                                                  (SQUARES_WIDTH - WUMPUS_SIZE) / 2),
                                              int(DEAD_WUMPUS[0] * SQUARES_WIDTH + WALL_WIDTH
                                                  + (SQUARES_WIDTH - WUMPUS_SIZE) / 2)))

        # agent(Steve)
        screen.blit(scaled_steve, (int(AGENT[1] * SQUARES_WIDTH + WALL_WIDTH + (SQUARES_WIDTH - AGENT_SIZE) / 2),
                                   int(AGENT[0] * SQUARES_WIDTH + WALL_WIDTH + (SQUARES_WIDTH - AGENT_SIZE) / 2)))

        pygame.time.delay(300)
        pygame.display.flip()


def drawGameOver():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 10))

        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('Game over.', True, (163, 0, 101), (0, 0, 10))
        textRect = text.get_rect()
        textRect.center = (SCREEN_SIZE // 2, SCREEN_SIZE // 2)
        screen.blit(text, textRect)
        pygame.display.flip()
    pygame.quit()


def drawWinner():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 10))
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('He found the diamonds and was happy ever after.', True, (163, 0, 101), (0, 0, 10))
        textRect = text.get_rect()
        textRect.center = (SCREEN_SIZE // 2, SCREEN_SIZE // 2)
        screen.blit(text, textRect)

        pygame.display.flip()
    pygame.quit()


def drawNoWay():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 10))
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('He is not brave enough to go further.', True, (163, 0, 101), (0, 0, 10))
        textRect = text.get_rect()
        textRect.center = (SCREEN_SIZE // 2, SCREEN_SIZE // 2)
        screen.blit(text, textRect)

        pygame.display.flip()
    pygame.quit()