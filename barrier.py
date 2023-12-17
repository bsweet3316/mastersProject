# -*- coding: utf-8 -*-
"""
Created on Sat Jul 22 16:00:05 2023

@author: starw
"""

import pygame
import math

class Barrier(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, blockType):
        super(Barrier, self).__init__()
        self.pos = (x,y)
        self.width = width
        self.height = height
        
        self.intersection = False
        self.color =  pygame.Color('brown')
        
        self.surface = pygame.Surface((width,height))
        self.blockType = blockType
        
        self.rect = self.surface.get_rect(topleft=self.pos)
        
    def draw(self, screen):
        if self.intersection == True:
            self.color = pygame.Color('blue')
        else:
            self.color = pygame.Color('brown')
        
        if self.blockType == 1:
            pygame.draw.rect(self.surface, self.color, \
                             (1, 1, self.width-2, self.height))
        elif self.blockType == 2:
            pygame.draw.polygon(self.surface, self.color, \
                            [(0, 0), (10, 10), (10, 0)])
        elif self.blockType == 3:
             pygame.draw.polygon(self.surface, self.color, \
                             [(0,0), (10, 10), (0, 10)])
        elif self.blockType == 4:
             pygame.draw.polygon(self.surface, self.color, \
                             [(10, 0), (10, 10), (0, 10)])
        elif self.blockType == 5:
             pygame.draw.polygon(self.surface, self.color, \
                             [(0, 0), (10, 0), (0, 10)])
        
        
        screen.blit(self.surface, self.rect)
        

    def checkLineOfSight(self, line):
        
        
        def linesAreParallel( x1,y1, x2,y2, x3,y3, x4,y4 ):
            """ Return True if the given lines (x1,y1)-(x2,y2) and
            (x3,y3)-(x4,y4) are parallel """
            amount = abs(((x1-x2)*(y3-y4)) - ((y1-y2)*(x3-x4)))
            return (amount == 0 or amount < 0.000001)

        def intersectionPoint( x1,y1, x2,y2, x3,y3, x4,y4 ):
            """ Return the point where the lines through (x1,y1)-(x2,y2)
            and (x3,y3)-(x4,y4) cross.  This may not be on-screen  """
            #Use determinant method, as per
            #Ref: https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection
            Px = ((((x1*y2)-(y1*x2))*(x3 - x4)) - ((x1-x2)*((x3*y4)-(y3*x4)))) / (((x1-x2)*(y3-y4)) - ((y1-y2)*(x3-x4)))
            Py = ((((x1*y2)-(y1*x2))*(y3 - y4)) - ((y1-y2)*((x3*y4)-(y3*x4)))) / (((x1-x2)*(y3-y4)) - ((y1-y2)*(x3-x4)))
            return Px,Py
        
        
        rect = self.rect
        result = []
        line_x1, line_y1, line_x2, line_y2 = line 
        pos_x, pos_y, width, height = rect


        
        rect_lines = [ ( pos_x, pos_y, pos_x+width, pos_y ), ( pos_x, pos_y+height, pos_x+width, pos_y+height ),  # top & bottom
                   ( pos_x, pos_y, pos_x, pos_y+height ), ( pos_x+width, pos_y, pos_x+width, pos_y+height ) ] # left & right
        
        for r in rect_lines:
            rx1,ry1,rx2,ry2 = r
            print(f'{rx1} {rx2} {ry1} {ry2}')
            if ( not linesAreParallel( line_x1,line_y1, line_x2,line_y2, rx1,ry1, rx2,ry2 ) ):    # not parallel
                pX, pY = intersectionPoint( line_x1,line_y1, line_x2,line_y2, rx1,ry1, rx2,ry2 )  # so intersecting somewhere
                
                pX = round( pX )
                pY = round( pY )
                
                print(f'{pX}  {pY}')
                print(rect.collidepoint( pX, pY ))
                
                print(f'MIN X: {min( line_x1, line_x2 )} Y: {min( line_y1, line_y2 )}')
                print(f'MAX X: {max( line_x1, line_x2 )} Y: {max( line_y1, line_y2 )}')

                
                # Lines intersect, but is on the rectangle, and between the line end-points?
                if ( pX >= min( rx1, rx2 ) and pX <= max( rx1, rx2 ) and
                    pY >= min( ry1, ry2 ) and pY <= max( ry1, ry2 )   and
                    pX >= min( line_x1, line_x2 ) and pX <= max( line_x1, line_x2 ) and
                    pY >= min( line_y1, line_y2 ) and pY <= max( line_y1, line_y2 ) ):
                    
                    
                    result.append( ( pX, pY ) )                                     # keep it
                    if ( len( result ) == 4 ):
                        break   # Once we've found 2 intersection points, that's it


        self.intersection = len(result) > 0
        
        return result
        
        