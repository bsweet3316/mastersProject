# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 09:13:34 2023

@author: starw
"""

import pygame
from pygame.math import Vector2


from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        
        super(Tank, self).__init__()
        self.pos = Vector2(x,y)
        self.color = color
        
        
        
        self.cannon = pygame.Surface((30, 10), pygame.SRCALPHA)
        pygame.draw.polygon(self.cannon, pygame.Color(color), 
                            [(0,0), (30, 5), (0, 10)])
        
        
        
        
        self.tank_body = pygame.Surface((40, 30), pygame.SRCALPHA)
        pygame.draw.polygon(self.tank_body, pygame.Color('blue'), 
                            [(0,5), (0, 25), (40,25), (40, 5)])
        pygame.draw.polygon(self.tank_body, pygame.Color('black'), 
                            [(0,3),(0,5),(7,5),((7,3))])
        pygame.draw.polygon(self.tank_body, pygame.Color('black'), 
                            [(33,3),(33,5),(40,5),((40,3))])
        pygame.draw.polygon(self.tank_body, pygame.Color('black'), 
                            [(33,25),(33,27),(40,27),((40,25))])
        pygame.draw.polygon(self.tank_body, pygame.Color('black'), 
                            [(0,25),(0,27),(7,27),((7,25))])
        
        
        self.body_pos = Vector2(x,y)
        self.direction = Vector2(1,0)
        self.speed = 0
        self.angle_speed = 0
        self.angle = 0
        
        
        self.orig_cannon = self.cannon
        self.orig_body = self.tank_body
        
        
        self.cannon_rect = self.cannon.get_rect(center=(x,y))
        self.rect = self.tank_body.get_rect(center=(x,y))
        
        self.player_cannon_angle = 0
        
        
        
    def update(self, barriers):

        if self.angle_speed != 0:
            self.direction.rotate_ip(self.angle_speed)
            self.angle += self.angle_speed
            self.tank_body = pygame.transform.rotate(self.orig_body, -self.angle)
            self.rect = self.tank_body.get_rect(center=self.rect.center)
        
        updateMovement = self.direction * self.speed
        
        self.body_pos += updateMovement
        self.rect.center = self.body_pos
        
        
        
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 1000:
            self.rect.right = 1000
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= 600:
            self.rect.bottom = 600
        
        for barrier in barriers:
            
            if self.rect.colliderect(barrier):
                self.body_pos -= updateMovement
                self.rect.center = self.body_pos

                
            
        self.cannon_rect.center = self.rect.center
        self.pos = self.body_pos
        
        
    def rotate(self):
        direction = pygame.mouse.get_pos() - self.pos
        radius, angle = direction.as_polar()
        
        self.player_cannon_angle = angle
        
        self.cannon = pygame.transform.rotate(self.orig_cannon, -angle)
        self.cannon_rect = self.cannon.get_rect(center=self.cannon_rect.center)
        
    def updateAndDraw(self, window, barriers):
        self.update(barriers)
        self.rotate()
        
        window.blit(self.tank_body, self.rect)
        window.blit(self.cannon, self.cannon_rect)
        
        
        
        