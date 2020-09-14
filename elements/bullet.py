# class bullet
import pygame
import numpy as np
from elements.define import *
vec = pygame.math.Vector2

class bullet(pygame.sprite.Sprite):
    def __init__(self, image_path, player, x, y, yaw, v=10):
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        self.yaw = yaw
        self.v = v
        self.image_path = image_path
        self.origin = pygame.image.load(self.image_path)
        self.image = pygame.transform.rotate(self.origin, yaw)
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.rect.center = self.pos
    
    def move(self):
        new_x = self.pos[0] - self.v * np.math.sin(self.yaw * 3.1415926 / 180)
        new_y = self.pos[1] - self.v * np.math.cos(self.yaw * 3.1415926 / 180)
        self.pos = vec(new_x, new_y)
        self.rect.center = self.pos
        


        