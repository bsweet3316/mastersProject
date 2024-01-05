# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 09:10:17 2023

@author: starw
"""

import pygame 
from tank import Tank
from cpu_tank import CpuTank
from bullet import Bullet
from barrier import Barrier
from barrier_map_generator import chooseRandomBoard
from nnSightLine import NNSightLine
from network import Network
import math
import time
import torch 


from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    KEYUP,
    QUIT,
)

BACKGROUND_COLOR =(255,255,255)


class TankGame():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000,600))

        self.all_sprites = []
        self.nonAiSprites = []
        self.bullets = []
        self.tanks = []
        self.barriers = []

        self.playerTank = Tank(500, 300, (0,0,0))

        self.cpuTank = CpuTank(200, 400, (255,255,0))

        self.timeSinceLastCpuShot = time.time()
        

        self.playerScore = 0
        self.cpuScore = 0


        

        self.tanks.append(self.playerTank)
        self.tanks.append(self.cpuTank)
            
        for tank in self.tanks: 
            self.nonAiSprites.append(tank)

        self.all_sprites.append(self.playerTank)
        

        self.barriers.append(Barrier(70,70,70,70,1))
        self.barriers.append(Barrier(70,460,70,70,1))
        self.barriers.append(Barrier(860,70,70,70,1))
        self.barriers.append(Barrier(860,460,70,70,1))

        self.barriers.append(Barrier(340,130,50,340,1))
        self.barriers.append(Barrier(610,130,50,340,1))

        for barrier in self.barriers:
            self.all_sprites.append(barrier)
            self.nonAiSprites.append(barrier)


        self.clock = pygame.time.Clock()

        pygame.font.init() 
        self.my_font = pygame.font.SysFont('Comic Sans MS', 30)



    def updateGame(self):
        running = True
        
        self.screen.fill(BACKGROUND_COLOR)
        inputs = [26]
        pressed_keys = pygame.key.get_pressed()
            # for loop through the event queue
        for event in pygame.event.get():
           # Check for KEYDOWN event
           if event.type == KEYDOWN:
               key = event.key
               if key == K_UP:
                   self.playerTank.speed = 3
               elif key == K_DOWN:
                   self.playerTank.speed = -1
               elif key == K_LEFT:
                   self.playerTank.angle_speed = -4
               elif key == K_RIGHT:
                   self.playerTank.angle_speed = 4
               # If the Esc key is pressed, then exit the main loop
               elif key == K_ESCAPE:
                   running = False
           elif event.type == KEYUP:
               if key == K_UP:
                   self.playerTank.speed = 0
               elif key == K_DOWN:
                   self.playerTank.speed = 0
               elif key == K_LEFT:
                   self.playerTank.angle_speed = 0
               elif key == K_RIGHT:
                   self.playerTank.angle_speed = 0
           elif event.type == pygame.MOUSEBUTTONDOWN:
               start_x, start_y = self.playerTank.pos
               mouse_x, mouse_y = event.pos

               dir_x, dir_y = mouse_x - start_x, mouse_y - start_y
               distance = math.sqrt(dir_x**2 + dir_y**2)
               if distance > 0:
                   new_bullet = Bullet(start_x, start_y, dir_x/distance, dir_y/distance, 1)
                   self.bullets.append(new_bullet)
                   self.nonAiSprites.append(new_bullet)
        # Check for QUIT event. If QUIT, then set running to false.
           elif event.type == QUIT:
               running = False
               
        
        fireBullet = self.cpuTank.cpuStateMachine(self.all_sprites, self.screen, self.playerTank, self.barriers)    
        if fireBullet and time.time() - self.timeSinceLastCpuShot > 1:
            angleToFire = math.radians(self.cpuTank.cannon_angle)
            new_bullet = Bullet(self.cpuTank.pos[0], self.cpuTank.pos[1], math.cos(angleToFire), math.sin(angleToFire), 2)
            self.bullets.append(new_bullet)
            self.nonAiSprites.append(new_bullet)
            self.timeSinceLastCpuShot = time.time()

        for bullet in self.bullets:
            bullet.move()
            bullet.draw(self.screen)
            if bullet.checkBoundary() or pygame.sprite.spritecollideany(bullet, self.barriers):
                self.bullets.pop(self.bullets.index(bullet))
                self.nonAiSprites.pop(self.nonAiSprites.index(bullet))
            elif pygame.sprite.collide_rect(bullet, self.cpuTank) and bullet.playerId != 2:
                self.playerScore = self.playerScore + 1
                self.bullets.pop(self.bullets.index(bullet))
                self.nonAiSprites.pop(self.nonAiSprites.index(bullet))

            elif pygame.sprite.collide_rect(bullet, self.playerTank) and bullet.playerId != 1:
                self.cpuScore = self.cpuScore + 1
                self.bullets.pop(self.bullets.index(bullet))
                self.nonAiSprites.pop(self.nonAiSprites.index(bullet))       
               
               
        self.playerTank.updateAndDraw(self.screen, self.barriers)
        
        intersectionFound = False
        for barrier in self.barriers:
            result = barrier.checkLineOfSight([self.cpuTank.pos[0], self.cpuTank.pos[1], self.playerTank.pos[0], self.playerTank.pos[1]])
            barrier.draw(self.screen)
            if len(result) > 0:
                intersectionFound = True
        
        
        self.cpuTank.checkLineOfSight(self.playerTank, intersectionFound)
        
            
        player_score_text = self.my_font.render(str(self.playerScore), False, (0, 0, 0))
        self.screen.blit(player_score_text, (20,20))
        cpu_score_text = self.my_font.render(str(self.cpuScore), False, (0, 0, 0))
        self.screen.blit(cpu_score_text, (920,20))



        pygame.display.flip()
        self.clock.tick(30)
        
        return running               




