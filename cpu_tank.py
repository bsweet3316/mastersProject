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

GRID_SIZE = 10

class CpuTank(Tank):
    
    def __init__(self, x, y, color):
        
        super(CpuTank, self).__init__(x, y, color)
        
        randX = random.randint(3, 97)
        randY = random.randint(3, 57)
        self.destination = (randX, randY)
        self.path = []
        self.state = 1
        self.destinationReached = True
        
    def chooseDestination(self, game_map): 
        valid = False
        
        newDest = (0,0)
        
        while not valid:
            randX = random.randint(3, 97)
            randY = random.randint(3, 57)
            newDest = (randX, randY)
            
            if game_map[randX][randY] == 0:
                valid = True
                
        self.destination = newDest
        print(self.destination)
        
        

    def generateMap(self, all_sprites, screen):
        
        m, n = int(1000/GRID_SIZE), int(600/GRID_SIZE)
        
        game_map = [[0] * n for i in range(m)]
        
        for sprite in all_sprites:
            
            topLeftX, topLeftY = sprite.rect.topleft
            topLeftX = int(topLeftX/GRID_SIZE)
            topLeftY = int(topLeftY/GRID_SIZE)
            
            bottomRightX, bottomRightY = sprite.rect.bottomright
            bottomRightX = int(bottomRightX/GRID_SIZE)
            bottomRightY = int(bottomRightY/GRID_SIZE)
            
            
            for i in range(topLeftX, bottomRightX+1):
                for j in range(topLeftY, bottomRightY+1):
                    game_map[i][j] = 1
        
        for j in range(0, len(game_map)):
            for i in range(0, len(game_map[0])):
                if game_map[j][i] == 0:
                    pygame.draw.rect(screen, pygame.Color('blue'), ((j*GRID_SIZE), (i*GRID_SIZE), GRID_SIZE, GRID_SIZE))
                else:
                    pygame.draw.rect(screen, pygame.Color('red'), ((j*GRID_SIZE), (i*GRID_SIZE), GRID_SIZE, GRID_SIZE))
                    
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
  
    
    def find_path(self, game_map):
        
        x,y = self.rect.center
        x = int(x/GRID_SIZE)
        y = int(y/GRID_SIZE)
        
        source =(x,y)
        
        path = self.bfs(game_map, source)
        
        return path
    
    def move_to_destination(self, path, screen):
        
        if len(path) == 1:
            return True
        
        x,y = self.pos
        
        
        next_point_x, next_point_y = path[0]
        x = math.floor(x/GRID_SIZE)
        y = math.floor(y/GRID_SIZE)
    
        if (x == next_point_x and y == next_point_y) and len(path) > 1:
            next_point_x, next_point_y = path[1]
            
        dx = next_point_x - x
        dy = next_point_y - y
        
        
        desired_angle = math.degrees(math.atan2(dy,dx))
        self.angle_speed = 0
        self.speed = 0
        
        curr_angle =self.angle
        
        if (curr_angle != int(desired_angle)):
            if curr_angle > desired_angle:    
                
                self.angle_speed = -3
            else:
                self.angle_speed = 3
        else:
            self.speed = 2
            
        self.updateAndDraw(screen)
        
        return False
        
    def cpuStateMachine(self, all_sprites, screen):
        game_map = self.generateMap(all_sprites, screen)
        
        print(self.state)
        if self.state == 1:
            if self.destinationReached:
                print('Choosing Dest')
                self.chooseDestination(game_map)
                self.destinationReached = False
            else:
                path = self.find_path(game_map)  
                for point in path:
                    pygame.draw.rect(screen, pygame.Color('green'), (point[0]*10, point[1]*10, 10, 10))
                
                self.destinationReached =  self.move_to_destination(path, screen)
        
            
            