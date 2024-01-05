# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 14:27:17 2023

@author: starw
"""
from tank import Tank
from nnSightLine import NNSightLine
from network import Network


class AgentTank(Tank):
    
    def __init__(self, state_size, action_size):
        super(AgentTank, self).__init__()
        
        self.cannon_angle = 0
        self.cannon_speed = 0
        self.sight_lines = []
        
        for i in range(0, 19):
            
            self.sight_lines.append(NNSightLine(i*5))
            
        self.state_size = state_size
        self.action_size = action_size
        
        self.local_network = Network(state_size, action_size)
        self.target_network = Network(state_size, action_size)
        
        self.t_step = 0