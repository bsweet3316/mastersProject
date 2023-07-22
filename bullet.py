# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 13:28:38 2023

@author: starw
"""
import pygame
from pygame.math import Vector2


def calc_new_xy(old_xy, speed, angle_in_degrees):
    move_vec = Vector2()
    move_vec.from_polar()

class Bullet(pygame.sprite.Sprite):
    
    def __init__(self, x, y, dirx, diry):
        super(Bullet, self).__init__()
        
        self.x = x
        self.y = y
        self.dirx = dirx
        self.diry = diry
        
        self.image = pygame.Surface((5,5))
        self.image.fill((255,0,0))
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

        
        self.speed = 5
        
    def move(self):
        self.x += self.dirx * self.speed
        self.y += self.diry * self.speed
        
    def draw(self, window):
        self.rect.topleft = (round(self.x), round(self.y))
        
        window.blit(self.image, self.rect)
        
    def checkBoundary(self):
        return self.x < 0 or self.x > 1000 or self.y < 0 or self.y > 600
        
        
        
        
        