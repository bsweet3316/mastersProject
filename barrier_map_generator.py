# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 15:03:49 2023

@author: starw
"""

import random
import csv

def chooseRandomBoard():
    
    
    board = []
    
    with open("Board5.csv") as csvfile:
        
        for line in csvfile.readlines():
            row = []
            for entry in line.split(','):
                row.append(int(entry))
            board.append(row)
                
    print(board)
    
    return board            
        
    