# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 16:38:39 2023

@author: starw
"""
from tank import Tank
import pygame
import collections
import math
import random

dRow = [ -1, 0, 1, 0]
dCol = [ 0, 1, 0, -1]

class CpuTank(Tank):
    
    def __init__(self, x, y, color):
        
        super(CpuTank, self).__init__(x, y, color)
        
        randX = random.randint(0, 50)
        randY = random.randint(0, 30)
        self.destination = (randX, randY)
        self.path = []
        
        

    def generateMap(self, all_sprites, screen):
        
        m, n = int(1000/20), int(600/20)
        
        game_map = [[0] * n for i in range(m)]
        
        for sprite in all_sprites:
            
            topLeftX, topLeftY = sprite.rect.topleft
            topLeftX = int(topLeftX/20)
            topLeftY = int(topLeftY/20)
            
            bottomRightX, bottomRightY = sprite.rect.bottomright
            bottomRightX = int(bottomRightX/20)
            bottomRightY = int(bottomRightY/20)
            
            
            for i in range(topLeftX, bottomRightX+1):
                for j in range(topLeftY, bottomRightY+1):
                    game_map[i][j] = 1
        
        for j in range(0, len(game_map)):
            for i in range(0, len(game_map[0])):
                if game_map[j][i] == 0:
                    pygame.draw.rect(screen, pygame.Color('blue'), ((j*20), (i*20), 20, 20))
                else:
                    pygame.draw.rect(screen, pygame.Color('red'), ((j*20), (i*20), 20, 20))
                    
        return game_map
        
    def is_valid_cell(self, x, y, game_map):
        valid = True
        
        if x < 0 or y < 0 or x >= len(game_map) or y >= len(game_map[0]):
            valid = False
        
        elif game_map[x][y] == 1:
            valid = False
        
        return valid
    
    
    def bfs(self, game_map, start):
        
        queue = collections.deque([[start]])
        seen = set([start])
        
        while queue:
            path = queue.popleft()
            x,y = path[-1]
            if (x,y) == self.destination:
                return path
            for x2, y2 in ((x+1, y), (x+1,y+1), (x-1, y), (x+1, y-1), (x, y+1), (x-1, y-1), (x,y-1), (x-1, y+1)):
                if self.is_valid_cell(x2, y2, game_map) and not (x2,y2) in seen:
                    queue.append(path + [(x2, y2)])
                    seen.add((x2, y2))
  
    
    def find_path(self, all_sprites, screen):
        game_map = self.generateMap(all_sprites, screen)
        
        x,y = self.rect.center
        x = int(x/20)
        y = int(y/20)
        
        source =(x,y)
        
        path = self.bfs(game_map, source)
        
        return path
    
    def move_to_destination(self, path, screen):
        
        print(path)
        x,y = self.pos
        
        
        next_point_x, next_point_y = path[0]
        x = math.floor(x/20)
        y = math.floor(y/20)
        print(f'{x}, {y}')
        if (x == next_point_x and y == next_point_y):
            print(f'PATH 1 chosen:  {path[1]}')
            next_point_x, next_point_y = path[1]
            
        dx = next_point_x - x
        dy = next_point_y - y
        
        print(f'NEXT:  {next_point_x},{next_point_y}')
        desired_angle = math.degrees(math.atan2(dy,dx))
        self.angle_speed = 0
        self.speed = 0
        
        curr_angle =self.angle
        
        print(f'current angle: {curr_angle}')
        print(f'Desired: {desired_angle}')
        if (curr_angle != int(desired_angle)):
            if curr_angle > desired_angle:    
                
                self.angle_speed = 3
            else:
                self.angle_speed = -3
        else:
            self.speed = 2
            
        self.updateAndDraw(screen)
        
        
        
    def get_angle_on_circle(self, angle):
        angle = abs(angle)
        print(angle)
        while angle < 0:
            angle = angle + 360
        while angle > 360:
            angle = angle - 360
            
                
        return angle
            
            