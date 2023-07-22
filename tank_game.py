# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 09:10:17 2023

@author: starw
"""

import pygame 
from tank import Tank
from cpu_tank import CpuTank
from bullet import Bullet
import math

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

pygame.init()
background_color = (255,255,255)


screen = pygame.display.set_mode((1000,600))

all_sprites = []

tank = Tank(500, 300, (0,0,0))

cpuTank = CpuTank(200, 400, (255,255,0))

bullets = []
tanks = []

tanks.append(tank)
tanks.append(cpuTank)

all_sprites.append(tank)

clock = pygame.time.Clock()

paths = cpuTank.find_path(all_sprites, screen)

print(paths)

running = True

while running:
    screen.fill(background_color)
    
    
        # for loop through the event queue
    for event in pygame.event.get():
       # Check for KEYDOWN event
       if event.type == KEYDOWN:
           key = event.key
           if key == K_UP:
               tank.speed = 3
           elif key == K_DOWN:
               tank.speed = -1
           elif key == K_LEFT:
               tank.angle_speed = -4
           elif key == K_RIGHT:
               tank.angle_speed = 4
           # If the Esc key is pressed, then exit the main loop
           elif key == K_ESCAPE:
               running = False
       elif event.type == KEYUP:
           if key == K_UP:
               tank.speed = 0
           elif key == K_DOWN:
               tank.speed = 0
           elif key == K_LEFT:
               tank.angle_speed = 0
           elif key == K_RIGHT:
               tank.angle_speed = 0
       elif event.type == pygame.MOUSEBUTTONDOWN:
           start_x, start_y = tank.pos
           mouse_x, mouse_y = event.pos

           dir_x, dir_y = mouse_x - start_x, mouse_y - start_y
           distance = math.sqrt(dir_x**2 + dir_y**2)
           if distance > 0:
               new_bullet = Bullet(start_x, start_y, dir_x/distance, dir_y/distance)
               bullets.append(new_bullet)
    # Check for QUIT event. If QUIT, then set running to false.
       elif event.type == QUIT:
           running = False
           
    pressed_keys = pygame.key.get_pressed()
    cpuTank.generateMap(all_sprites,screen)
    
    paths = cpuTank.find_path(all_sprites, screen)
    cpuTank.move_to_destination(paths, screen)
    
    for point in paths:
        pygame.draw.rect(screen, pygame.Color('green'), (point[0] * 20, point[1] * 20, 20, 20))


    for bullet in bullets:
        bullet.move()
        bullet.draw(screen)
        
        if bullet.checkBoundary():
            bullets.pop(bullets.index(bullet))
            
    tank.updateAndDraw(screen)

        



    pygame.display.flip()
    clock.tick(30)


pygame.quit()
