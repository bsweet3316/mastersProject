# -*- coding: utf-8 -*-
"""
Created on Sat Jul 22 16:00:05 2023

@author: starw
"""

import pygame

class Barrier(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Barrier, self).__init__()
        self.pos = (x,y)
        
        
        self.surface = pygame.Surface((10,10))
        pygame.draw.rect(self.surface, pygame.Color('brown'), (x, y, 10,10))
        
        
        self.rect = self.surface.get_rect(center=self.pos)