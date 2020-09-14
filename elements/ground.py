# class block
import pygame
from elements.block import block
from elements.define import *
class ground(pygame.sprite.Sprite):
    def __init__(self, image_path):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.block_group = pygame.sprite.Group()
        self.block_group.add(block(10, 110, 100, 20))
        self.block_group.add(block(160, 420, 20, 100))
        self.block_group.add(block(160, 255, 100, 20))
        self.block_group.add(block(365, 110, 100, 20))
        self.block_group.add(block(405, 255, 20, 20))
        self.block_group.add(block(365, 400, 100, 20))
        self.block_group.add(block(570, 255, 100, 20))
        self.block_group.add(block(650, 10, 20, 100))
        self.block_group.add(block(720, 400, 100, 20))

        self.block_group.add(block(0, 0, 830, 10))
        self.block_group.add(block(0, 10, 10, 510))
        self.block_group.add(block(0, 520, 830, 10))
        self.block_group.add(block(820, 10, 10, 510))