import pygame, csv, os

from pygame.sprite import _Group

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, spritesheet):
        pygame.sprite.Sprite.__init__(self)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        