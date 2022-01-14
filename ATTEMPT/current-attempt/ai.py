from json import detect_encoding
from turtle import width
from numpy.lib.function_base import copy
import pygame
import copy
import random
from piece import *
    
    
class Event: #Class that handles keys in for the AI
    type = None
    key = None

    def __init__(self, type, key):
        self.type = type
        self.key = key

class AI:
    def detectCollision(self, piece): #COPIED FROM THE TETRIS FILE (MAIN PROGRAM) AND MODIFIED SLIGHTLY
        values = piece.get()
        for block in values:
            a, b = block
            if a > self.width-1 or a < 0 or b > self.height-1 or block in self.positions:
                return True       
        return False
    
    def bounds(self, x, y):
        if x>=0 and y>=0 and x<self.width and y<self.height: return True
        else: return False
    
    def removePiece(self, piece, grid):
        for block in piece.get():
            x, y = block
            if x>=0 and y>=0:
                grid[x][y] = 0
        return grid
    
    def __init__(self) -> None:
        self.target: Piece = None
    
    def proc(self, grid, piece, positions, width, height, new_target):
        
        #import and define all needed variables
        self.width = width
        self.height = height
        self.piece = copy.deepcopy(piece)
        self.grid = grid
        self.positions = positions
        
        #calculates the best move and records the postition if needed
        if new_target:
            self.target = copy.deepcopy(self.getTarget())
            new_target = False
        
        x, y = self.piece.anchor
        xt, yt = self.target.anchor
        
        e = Event(pygame.KEYDOWN, pygame.K_s)
        
        if self.piece.raw() != self.target.raw():
            e =Event(pygame.KEYDOWN, pygame.K_UP)
        #move left if needed
        elif x > xt:
            e = Event(pygame.KEYDOWN, pygame.K_LEFT)
            
        #move right if needed
        elif x < xt:
            e = Event(pygame.KEYDOWN, pygame.K_RIGHT)
            
        #move down if needed
        elif y < yt:
            e = Event(pygame.KEYDOWN, pygame.K_DOWN)
            
        return [e]
            
    def getTarget(self):
        moves = []
        
        #create needed copies of the piece
        default = copy.deepcopy(self.piece)
        end = False
        self.grid = self.removePiece(self.piece, self.grid)
        
        #moves the piece to the very left and above the right
        default.anchor = (1,-5)
        while not self.detectCollision(default):
            default.left()
        default.right()
        
        while not end:
            
            #move the piece down until it can't
            current = copy.deepcopy(default)
            for i in range(4):
                current.rotate()
                if self.detectCollision(current):
                    for _ in range(3): current.rotate()
                while not self.detectCollision(current):
                    current.down()
                current.up()
                
                #adds the move to the list of all moves
                moves.append(copy.deepcopy(current))
            
            #moves the default piece to the right
            default.right()
            
            #ends the program if the default piece is out of bounds
            if self.detectCollision(default):
                end = True
        
        heights = self.getHeight(moves)
        holes = self.getHoles(moves)
        againsts = self.getAgainst(moves)
        blockades = self.getBlockades(moves)
        lines_cleared = self.getLinesCleared(moves)
        suits = []
        for i in range(len(moves)):
            suit = 0 - heights[i] - 3*holes[i] + 0.2*againsts[i] - 30*blockades[i] + 4**lines_cleared[i]
            suits.append(suit)
        index = suits.index(max(suits))
        return moves[index]
          
    def getHeight(self, moves):
        
        #empty list of heights for each move
        heights = []
        for piece in moves:
            
            #place the piece in the grid
            for block in piece.get():
                x, y = block
                if self.bounds(x, y):
                    self.grid[x][y] = piece.colour

            #calculate the max height for the move
            height = 0
            for y in range(self.height-1, 0, -1):
                for x in range(self.width):
                    if self.grid[x][y] != 0:
                        height = self.height - y

            #remove the piece from the grid
            for block in piece.get():
                x, y = block
                if self.bounds(x, y):
                    self.grid[x][y] = 0
                
            heights.append(height)
        return heights
    
    def getHoles(self, moves):
        
        #empty list of holes for each move
        holes = []
        for piece in moves:
            
            #place the piece in the grid
            for block in piece.get():
                x, y = block
                if self.bounds(x, y):
                    self.grid[x][y] = piece.colour

            #calculate the number of holes
            hole = 0
            for y in range(self.height-1, 1, -1):
                for x in range(self.width):
                    if self.grid[x][y] == 0 and self.grid[x][y-1] != 0:
                        hole += 1

            #remove the piece from the grid
            for block in piece.get():
                x, y = block
                if self.bounds(x, y):
                    self.grid[x][y] = 0
                
            holes.append(hole)
        return holes          
            
    def getAgainst(self, moves):
        
        #empty list of heights for each move
        againsts = []
        for piece in moves:
            
            #place the piece in the grid
            for block in piece.get():
                x, y = block
                if self.bounds(x, y):
                    self.grid[x][y] = piece.colour

            #calculate how many blocks/sides of the grid the block is touching
            against = 0
            for block in piece.get():
                x, y = block
                if x == 0:
                    against += 1
                if x == self.width-1:
                    against += 1
                if y == self.height-1:
                    against += 1
                if self.bounds(x-1, y):
                    if self.grid[x-1][y] != 0:
                        against += 1
                if self.bounds(x+1, y):
                    if self.grid[x+1][y]:
                        against += 1
                if self.bounds(x, y+1):
                    if self.grid[x][y+1]:
                        against +=1     

            #remove the piece from the grid
            for block in piece.get():
                x, y = block
                if self.bounds(x, y):
                    self.grid[x][y] = 0
                
            againsts.append(against)
        return againsts
    
    def getBlockades(self, moves):
        blockades = []
        for piece in moves:
            
            #place the piece in the grid
            for block in piece.get():
                x, y = block
                if self.bounds(x, y):
                    self.grid[x][y] = piece.colour

            #calculate if there is a blockade(piece on top of a hole)
            blockade = 0
            for y in range(self.height-1, 1, -1):
                for x in range(self.width):
                    if self.grid[x][y] == 0 and self.grid[x][y-1] != 0:
                        for block in piece.get():
                            x1, y1 = block
                            if x == x1:
                                blockade = 1 

            #remove the piece from the grid
            for block in piece.get():
                x, y = block
                if self.bounds(x, y):
                    self.grid[x][y] = 0
                
            blockades.append(blockade)
        return blockades
    
    def getLinesCleared(self, moves):
       
        #empty list of lines cleared for each move
        lines = []
        for piece in moves:
            
            #place the piece in the grid
            for block in piece.get():
                x, y = block
                if self.bounds(x, y):
                    self.grid[x][y] = piece.colour

            #calculate the max height for the move
            lines_cleared = 0
            for y in range(self.height):
                count = 0
                for x in range(self.width):
                    if self.grid[x][y] != 0:
                        count += 1
                if count == self.width:
                    lines_cleared += 1
            
            
            #remove the piece from the grid
            for block in piece.get():
                x, y = block
                if self.bounds(x, y):
                    self.grid[x][y] = 0
                
            lines.append(lines_cleared)
        return lines 
    
    