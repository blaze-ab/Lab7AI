import pygame
import random
import os

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()

WALL_WIDTH = 20
SCREEN_SIZE = 780+WALL_WIDTH

SQUARES_NUM = 4
SQUARES_WIDTH = SCREEN_SIZE/SQUARES_NUM

FLOOR_HEIGHT = 50
GOLD_RADIUS = 50
HOLE_RADIUS = 90

current_path = os.path.dirname(__file__)

# Set up the drawing window
screen = pygame.display.set_mode([SCREEN_SIZE, SCREEN_SIZE])
running = True

gold_i = random.randint(0, SQUARES_NUM-1)
gold_j = random.randint(0, SQUARES_NUM-1)

while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((0, 0, 10))

    # walls
    pygame.draw.rect(screen, (89, 36, 36), (0, 0, SCREEN_SIZE, WALL_WIDTH))
    pygame.draw.rect(screen, (89, 36, 36), (0, 0, WALL_WIDTH, SCREEN_SIZE))
    pygame.draw.rect(screen, (89, 36, 36), (SCREEN_SIZE-WALL_WIDTH, 0, SCREEN_SIZE, SCREEN_SIZE))
    pygame.draw.rect(screen, (89, 36, 36), (0, SCREEN_SIZE-WALL_WIDTH, SCREEN_SIZE, SCREEN_SIZE))

    # lines vertical
    pygame.draw.line(screen, (89, 36, 36), (SQUARES_WIDTH, 0), (SQUARES_WIDTH, SCREEN_SIZE))
    pygame.draw.line(screen, (89, 36, 36), (2*SQUARES_WIDTH, 0), (2*SQUARES_WIDTH, SCREEN_SIZE))
    pygame.draw.line(screen, (89, 36, 36), (3*SQUARES_WIDTH, 0), (3*SQUARES_WIDTH, SCREEN_SIZE))

    # lines horizontal
    pygame.draw.line(screen, (89, 36, 36), (0, SQUARES_WIDTH), (SCREEN_SIZE, SQUARES_WIDTH))
    pygame.draw.line(screen, (89, 36, 36), (0, 2*SQUARES_WIDTH), (SCREEN_SIZE, 2*SQUARES_WIDTH))
    pygame.draw.line(screen, (89, 36, 36), (0, 3*SQUARES_WIDTH), (SCREEN_SIZE, 3*SQUARES_WIDTH))

    # pygame.draw.rect(screen, (89, 36, 36), (SCREEN_WIDTH-WALL_WIDTH, 0, SCREEN_WIDTH, SCREEN_HEIGHT - FLOOR_HEIGHT))

    # gold
    pygame.draw.circle(screen, (200, 130, 0), (int(gold_i*SQUARES_WIDTH+GOLD_RADIUS*2),
                                               int(gold_j*SQUARES_WIDTH+GOLD_RADIUS*2)), GOLD_RADIUS)

    # hole
    pygame.draw.circle(screen, (255, 255, 255), (int(2 * SQUARES_WIDTH + HOLE_RADIUS +
                                                     (SQUARES_WIDTH - 2*HOLE_RADIUS)/2),
                                                 int(2 * SQUARES_WIDTH + HOLE_RADIUS +
                                                     (SQUARES_WIDTH - 2*HOLE_RADIUS)/2)), HOLE_RADIUS)


    # Draw a solid blue circle in the center
    # pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)
    # pygame.draw.rect(screen, (0, 255, 0), (0, SCREEN_HEIGHT-FLOOR_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT))

    # coins = pygame.image.load(os.path.join(current_path, 'coin.bpm'))
    # coins.set_colorkey((255, 255, 255))

    '''
    for i in range(0, SCREEN_WIDTH, int(HOLE_WIDTH)):
        if i == 0 or i == SCREEN_WIDTH-HOLE_WIDTH or bool(random.getrandbits(1)):
            pygame.draw.rect(screen, (0, 255, 0), (i, SCREEN_HEIGHT - FLOOR_HEIGHT, i+int(HOLE_WIDTH), SCREEN_HEIGHT))
    '''
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
