# class block
import pygame
from elements.define import *

class block(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, color=blue):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
