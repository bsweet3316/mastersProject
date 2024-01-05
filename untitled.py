# -*- coding: utf-8 -*-
"""
Created on Sun Dec 24 15:12:14 2023

@author: starw
"""
import pygame

from tank_game import TankGame

if __name__ == "__main__":
    tankGame = TankGame()
    
    
    running = True;
    
    while running: 
        running = tankGame.updateGame()
    
    pygame.quit()