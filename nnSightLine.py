# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 18:48:52 2023

@author: starw
"""
import math 
from barrier import Barrier
import pygame

VIEW_LENGTH = 500

class NNSightLine:
    def __init__(self, angle):
        self.angle = angle
        self.length = VIEW_LENGTH
        
    
    def updateDistance(self, playerX, playerY, player_angle, sprites, window):
        destX = playerX + VIEW_LENGTH*math.cos(math.radians(player_angle + self.angle))
        destY = playerY + VIEW_LENGTH*math.sin(math.radians(player_angle + self.angle))

        self.length = VIEW_LENGTH
        intersectionFound = False
        for sprite in sprites:
            intersectionPoint = self.checkLineOfSight([round(playerX), round(playerY), round(destX), round(destY)], sprite)

            if (len(intersectionPoint) > 0):
                for point in intersectionPoint:
                    intersectionFound = True
                    newlength = math.sqrt(math.pow(point[0] - playerX, 2) + math.pow(point[1] - playerY, 2))        
                    if newlength <= self.length:
                        self.length = newlength
                        
        if not intersectionFound: 
            self.length = VIEW_LENGTH
        
        
            
        
        destX = playerX + self.length*math.cos(math.radians(player_angle + self.angle))
        destY = playerY + self.length*math.sin(math.radians(player_angle + self.angle))
        
        pygame.draw.line(window, pygame.Color('black'), (playerX, playerY), (destX, destY))
        pygame.draw.circle(window, pygame.Color('black'), (destX, destY), 2)
        
        
    def checkLineOfSight(self, line, sprite):
        
        
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
        
        
        rect = sprite.rect
        result = []
        line_x1, line_y1, line_x2, line_y2 = line 
        pos_x, pos_y, width, height = rect


        
        rect_lines = [ ( pos_x, pos_y, pos_x+width, pos_y ), ( pos_x, pos_y+height, pos_x+width, pos_y+height ),  # top & bottom
                   ( pos_x, pos_y, pos_x, pos_y+height ), ( pos_x+width, pos_y, pos_x+width, pos_y+height ) ] # left & right
        
        for r in rect_lines:
            rx1,ry1,rx2,ry2 = r
            if ( not linesAreParallel( line_x1,line_y1, line_x2,line_y2, rx1,ry1, rx2,ry2 ) ):    # not parallel
                pX, pY = intersectionPoint( line_x1,line_y1, line_x2,line_y2, rx1,ry1, rx2,ry2 )  # so intersecting somewhere
                
                pX = round( pX )
                pY = round( pY )

                
                # Lines intersect, but is on the rectangle, and between the line end-points?
                if ( pX >= min( rx1, rx2 ) and pX <= max( rx1, rx2 ) and
                    pY >= min( ry1, ry2 ) and pY <= max( ry1, ry2 )   and
                    pX >= min( line_x1, line_x2 ) and pX <= max( line_x1, line_x2 ) and
                    pY >= min( line_y1, line_y2 ) and pY <= max( line_y1, line_y2 ) ):
                    
                    
                    result.append( ( pX, pY ) )                                     # keep it
                    if ( len( result ) == 4 ):
                        break   # Once we've found 2 intersection points, that's it
        return result