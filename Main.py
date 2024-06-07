from Tiles import *
import pygame

pygame.init()
DISPLAY_W, DISPLAY_H = 800, 400
screen = pygame.display.set_mode((DISPLAY_W, DISPLAY_H))
clock = pygame.time.Clock()
running = True
dt = 0

map = TileMap('TestLevel.csv', )


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()