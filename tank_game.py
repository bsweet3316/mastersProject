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
import math
import time

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
nonAiSprites = []

tank = Tank(500, 300, (0,0,0))

cpuTank = CpuTank(200, 400, (255,255,0))

timeSinceLastShot = time.time()

playerScore = 0
cpuScore = 0


bullets = []
tanks = []
barriers = []

tanks.append(tank)
tanks.append(cpuTank)

nonAiSprites.append(cpuTank)

all_sprites.append(tank)
board = chooseRandomBoard()


barriers.append(Barrier(70,70,70,70,1))
barriers.append(Barrier(70,460,70,70,1))
barriers.append(Barrier(860,70,70,70,1))
barriers.append(Barrier(860,460,70,70,1))

barriers.append(Barrier(340,130,50,340,1))
barriers.append(Barrier(610,130,50,340,1))

for barrier in barriers:
    all_sprites.append(barrier)
    nonAiSprites.append(barrier)


clock = pygame.time.Clock()

pygame.font.init() 
my_font = pygame.font.SysFont('Comic Sans MS', 30)

sightLines = []

for i in range(0, 19):
    
    sightLines.append(NNSightLine(i*5))


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
               new_bullet = Bullet(start_x, start_y, dir_x/distance, dir_y/distance, 1)
               bullets.append(new_bullet)
               nonAiSprites.append(new_bullet)
    # Check for QUIT event. If QUIT, then set running to false.
       elif event.type == QUIT:
           running = False
           
    pressed_keys = pygame.key.get_pressed()
    fireBullet = cpuTank.cpuStateMachine(all_sprites, screen, tank, barriers)    
    if fireBullet and time.time() - timeSinceLastShot > 1:
        angleToFire = math.radians(cpuTank.cannon_angle)
        new_bullet = Bullet(cpuTank.pos[0], cpuTank.pos[1], math.cos(angleToFire), math.sin(angleToFire), 2)
        bullets.append(new_bullet)
        nonAiSprites.append(new_bullet)
        timeSinceLastShot = time.time()

    for bullet in bullets:
        bullet.move()
        bullet.draw(screen)
        if bullet.checkBoundary() or pygame.sprite.spritecollideany(bullet, barriers):
            bullets.pop(bullets.index(bullet))
            nonAiSprites.pop(nonAiSprites.index(bullet))
        elif pygame.sprite.collide_rect(bullet, cpuTank) and bullet.playerId != 2:
            playerScore = playerScore + 1
            bullets.pop(bullets.index(bullet))
            nonAiSprites.pop(nonAiSprites.index(bullet))

        elif pygame.sprite.collide_rect(bullet, tank) and bullet.playerId != 1:
            cpuScore = cpuScore + 1
            bullets.pop(bullets.index(bullet))
            nonAiSprites.pop(nonAiSprites.index(bullet))

            
            
    tank.updateAndDraw(screen, barriers)
    
    intersectionFound = False
    for barrier in barriers:
        result = barrier.checkLineOfSight([cpuTank.pos[0], cpuTank.pos[1], tank.pos[0], tank.pos[1]])
        barrier.draw(screen)
        if len(result) > 0:
            intersectionFound = True
    for sightLine in sightLines:
        sightLine.updateDistance(tank.pos[0], tank.pos[1], tank.player_cannon_angle-45, nonAiSprites, screen)
        
    cpuTank.checkLineOfSight(tank, intersectionFound)
    pygame.draw.line(screen, pygame.Color('red'), cpuTank.pos, tank.pos)
        
    player_score_text = my_font.render(str(playerScore), False, (0, 0, 0))
    screen.blit(player_score_text, (20,20))
    cpu_score_text = my_font.render(str(cpuScore), False, (0, 0, 0))
    screen.blit(cpu_score_text, (920,20))



    pygame.display.flip()
    clock.tick(30)


pygame.quit()
