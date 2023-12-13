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
VIEW_ANGLE = 40
VIEW_LENGTH = 350


class CpuTank(Tank):
    
    def __init__(self, x, y, color):
        
        super(CpuTank, self).__init__(x, y, color)
        
        randX = random.randint(3, 97)
        randY = random.randint(3, 57)
        self.destination = (randX, randY)
        self.path = []
        self.state = 1
        self.destinationReached = True
        self.cannon_angle = 0
        self.cannon_speed = 0
        
        self.amountToTurn = random.randint(-50,50)
        print(self.amountToTurn)
        
        
    def updateAndDraw(self, window, barriers):
        super(CpuTank, self).updateAndDraw(window, barriers)
        
        
        left_point_deltaX = VIEW_LENGTH*math.cos(math.radians(self.cannon_angle - VIEW_ANGLE))
        left_point_deltaY = VIEW_LENGTH*math.sin(math.radians(self.cannon_angle - VIEW_ANGLE))
        
        right_point_deltaX = VIEW_LENGTH*math.cos(math.radians(self.cannon_angle + VIEW_ANGLE))
        right_point_deltaY = VIEW_LENGTH*math.sin(math.radians(self.cannon_angle + VIEW_ANGLE))
        
        left_point = (self.pos[0] + left_point_deltaX, self.pos[1] + left_point_deltaY)
        right_point = (self.pos[0] + right_point_deltaX, self.pos[1] + right_point_deltaY)
        
        pygame.draw.line(window, pygame.Color('orange'), self.pos, left_point)
        pygame.draw.line(window, pygame.Color('orange'), self.pos, right_point)

        
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
        
    def rotate(self):
        if self.state == 1:
            self.cannon_speed = 0
            if self.amountToTurn == 0:
                self.amountToTurn = random.randint(-50,50)
            elif self.amountToTurn > 0:
                self.cannon_speed = -1
            else:
                self.cannon_speed = 1
                
        self.cannon_angle = self.cannon_angle + self.cannon_speed
        self.amountToTurn = self.amountToTurn + self.cannon_speed
        
        self.cannon = pygame.transform.rotate(self.orig_cannon, -self.cannon_angle)
        self.cannon_rect = self.cannon.get_rect(center=self.cannon_rect.center)    
         
            
        

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
            
        
            for i in range(topLeftX-1, bottomRightX+2):
                for j in range(topLeftY-1, bottomRightY+2):
                    if 0 < i < len(game_map) and 0 < j < len(game_map[0]):
                        game_map[i][j] = 1
                    
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
            for x2, y2 in ((x+1, y),  (x-1, y), (x, y+1), (x,y-1)):
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
        
        desired_angle = self.normalize_angle(math.degrees(math.atan2(dy,dx)))
        self.angle_speed = 0
        self.speed = 0
        
        curr_angle = self.normalize_angle(self.angle)
            
        if (curr_angle != int(desired_angle)):
            
            print(f'{curr_angle}  target: {desired_angle}')
            
            diff = abs(curr_angle - desired_angle)
            print(f'dist to desired {diff} other way: {360-diff}')
            if curr_angle > desired_angle:    
                if (360-diff) > diff:
                    self.angle_speed = -3
                else:
                    self.angle_speed = 3
                
            else:
                if (360-diff) > diff:
                    self.angle_speed = 3
                else:
                    self.angle_speed = -3
        else:
            self.speed = 2
            
        
        return False
    
    def checkLineOfSight(self, enemy_tank, intersectionFound):
        
        direction = enemy_tank.pos - self.pos
        radius, angle = direction.as_polar()
        
        left_angle = self.cannon_angle + VIEW_ANGLE
        right_angle = self.cannon_angle - VIEW_ANGLE
                
        angle = self.normalize_angle(angle)
        left_angle = self.normalize_angle(left_angle)
        right_angle = self.normalize_angle(right_angle)
        
        
        if not intersectionFound:
            print(f'{left_angle}  {angle}  {left_angle - VIEW_ANGLE*2}')
            if  (left_angle > angle > (left_angle - VIEW_ANGLE*2) or (right_angle + VIEW_ANGLE*2) < angle < right_angle) and radius <= VIEW_LENGTH:
                self.angle_speed = 0
                self.speed = 0
                self.state = 2
            else:
                self.angle_speed = 0
                self.speed = 0
                self.state = 1
        else: 
            self.state = 1
        
        
        
    def cpuStateMachine(self, all_sprites, screen, enemy_tank, barriers):
        game_map = self.generateMap(all_sprites, screen)
        shoot = False
        if self.state == 1:
            if self.destinationReached or game_map[self.destination[0]][self.destination[1]] == 1:
                self.chooseDestination(game_map)
                self.destinationReached = False
            else:
                path = self.find_path(game_map)  
                for point in path:
                    pygame.draw.rect(screen, pygame.Color('green'), (point[0]*10, point[1]*10, 10, 10))
                
                self.destinationReached =  self.move_to_destination(path, screen)

        elif self.state == 2:
            self.destinationReached = True
            
            direction = enemy_tank.pos - self.pos
            radius, angleToEnemy = direction.as_polar()
            angleToEnemy = self.normalize_angle(angleToEnemy)
            cannon_angle = self.normalize_angle(self.cannon_angle)
            tank_angle = self.normalize_angle(self.angle)
            
            if abs(cannon_angle - angleToEnemy) < 10:
                self.cannon_speed = 0
                shoot = True
            else:
                if cannon_angle > angleToEnemy:
                    self.cannon_speed = -2
                else: 
                    self.cannon_speed = 2
            
            if abs(tank_angle - angleToEnemy) < 5:
                self.angle_speed = 0
            else:
                if tank_angle > angleToEnemy:
                    self.angle_speed = -3
                else: 
                    self.angle_speed = 3
            
            if radius > VIEW_LENGTH/3:
                self.speed = 3
            else:
                self.speed = 0
            
        self.updateAndDraw(screen, barriers)
        return shoot
           
            
                
    def normalize_angle(self, angle):
        while angle <= 0:
            angle = angle + 360
            
        while angle > 360:
            angle = angle - 360
            
        return angle
        
            
            