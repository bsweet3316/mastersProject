# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 18:48:52 2023

@author: starw
"""
import math 
from barrier import Barrier
import pygame

class NNSightLine:
    def __init__(self, angle):
        self.angle = angle
        self.length = 300
        
    
    def updateDistance(self, playerX, playerY, player_angle, barriers, window):
        destX = playerX + 300*math.cos(math.radians(player_angle + self.angle))
        destY = playerY + 300*math.sin(math.radians(player_angle + self.angle))

        self.length = 300
        intersectionFound = False
        for barrier in barriers:
            intersectionPoint = barrier.checkLineOfSight([round(playerX), round(playerY), round(destX), round(destY)])
            print(f'PLAYER LINE:  {playerX} {playerY} {destX} {destY}')
            print('---------------------------------------------------')

            if (len(intersectionPoint) > 0):
                print(intersectionPoint)
                for point in intersectionPoint:
                    intersectionFound = True
                    pygame.draw.circle(window, pygame.Color('green'), (point[0], point[1]), 4)
                    newlength = math.sqrt(math.pow(point[0] - playerX, 2) + math.pow(point[1] - playerY, 2))        
                    if newlength <= self.length:
                        
                        self.length = newlength
                
        if not intersectionFound: 
            self.length = 300
            
        
        destX = playerX + self.length*math.cos(math.radians(player_angle + self.angle))
        destY = playerY + self.length*math.sin(math.radians(player_angle + self.angle))
        
        pygame.draw.line(window, pygame.Color('black'), (playerX, playerY), (destX, destY))
        pygame.draw.circle(window, pygame.Color('black'), (destX, destY), 2)