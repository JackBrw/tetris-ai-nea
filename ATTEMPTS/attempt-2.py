from re import X
from typing import Match
import pygame, sys, math, time
from pygame.locals import *
import numpy as np
import random as rd

colour = {   #Dictionary holding all required colour values
    "black":(0, 0, 0),
    "white":(255, 255, 255),
    "red":(255, 0, 0),
    "green":(0, 255, 0),
    "blue":(0, 0, 255)
}

def figures(figure): # holds the 7 grid positions for the pieces
    figures = (
        (1, 5, 9, 13), #I piece [0]
        (0, 4, 5, 6), #J piece [1]
        (0, 1, 2, 4), #L piece [2]
        (5, 6, 9, 10), #O piece [3]
        (1, 2, 4, 5), #S piece [4]
        (1, 4, 5, 6), #T piece [5]
        (0, 1, 5, 6) #Z piece [6]
    )
    if figure == -1:
        return figures[rd.randint(0, 6)]
    else:
        return figures[figure]


class Piece: # * The class that holds a matrix of the piece
    def __init__(self, typeVal, anchor) -> None: #initialiser, converts the array of numbers into a 4x4 matrix
        self.moving = True
        self.anchor = anchor
        self.values = figures(typeVal)
        self.matrix = np.array([[0, 0, 0, 0],
                               [0, 0, 0 ,0],
                               [0, 0, 0, 0],
                               [0, 0, 0, 0]])
        a, b, c, d = self.values
        for x in range(0, 4):
            for y in range(0, 4):
                if (x*4 + y) == a:
                    self.matrix[x, y] = 1
                if (x*4 + y) == b:
                    self.matrix[x, y] = 1
                if (x*4 + y) == c:
                    self.matrix[x, y] = 1
                if (x*4 + y) == d:
                    self.matrix[x, y] = 1
                    
    def get(self):
        return self.position()
                    
    def rotate(self): #rotate the matrix
        tempMat = self.matrix
        tempMat = np.transpose(tempMat)
        tempMat = np.flip(tempMat, 1)
        self.matrix = tempMat
        
    def position(self) -> list: #WIP
        val = []
        a, b = self.anchor
        for x in range(4):
            for y in range(4):
                if self.matrix[x][y] == 1:
                    val.append((x + a, y + b))
        return val
    
    def down(self):
        a, b = self.anchor
        b += 1
        self.anchor = (a, b)
        
    def lower_bound(self):
        a,b = self.anchor
        num = 0
        for x in range(3, 0, -1):
            if self.matrix[0][x] == 1:
                if x >= num : num = x
            if self.matrix[1][x] == 1:
                if x >= num : num = x
            if self.matrix[2][x] == 1:
                if x >= num : num = x
            if self.matrix[3][x] == 1:
                if x >= num : num = x
        return (num + b)
                    
    
class Tetris:
    def __init__(self, width, height) -> None: #initialiser
        self.height = height
        self.width = width
        self.positions = {}
        self.grid = []
        self.current_piece = None
        
    def create_grid(self, positions: dict) -> list: #creates the grid i.e sets the colour values
        grid = [[colour["white"] for _ in range(self.height)] for _ in range(self.width)]
        for x in range(len(grid)):
            for y in range(len(grid[x])):
                if (x, y) in positions:
                    grid[x][y] = positions[(x, y)]
        return grid
    
    def place_piece(self, piece: Piece, positions: dict):
        for x in range(len(piece.get())):
            positions[piece.get()[x]] = colour["red"]
        return positions
    
    def remove_piece(self, piece: Piece, positions: dict):
        for x in range(len(piece.get())):
            positions[piece.get()[x]] = colour["white"]
        return positions
    
    def main(self):
        run = True
        pygame.init()
        s_width = 350
        s_height = 600
        buffer = s_width / 8 - ((s_width / 8) % 10)
        win = pygame.display.set_mode((s_width, s_height))
        block_size = (s_height - 2*buffer)/ self.height
        piece_moving = False
        count = 0
        self.current_piece = Piece(-1, (3, -3))
        while run == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.display.quit()
                    quit()
                    
            if count > 500:
                if self.current_piece.moving == False:
                    self.current_piece = Piece(-1, (3,-3))
                    self.current_piece.moving = True
                else:
                    self.positions = self.place_piece(self.current_piece, self.positions)
                #----------------------------------
                if ((self.current_piece.lower_bound()) + 1) <= 19:
                    self.positions = self.remove_piece(self.current_piece, self.positions)
                    self.current_piece.down()
                else:
                    self.current_piece.moving = False
                #---------------------------------
                self.positions = self.place_piece(self.current_piece, self.positions)
                count = 0
                
            self.grid = self.create_grid(self.positions)
            
            for x in range(self.width): #draw the grid from the dictionary
                for y in range (self.height):
                    pygame.draw.rect(win, self.grid[x][y] , ((buffer + x*block_size), (buffer + y*block_size), block_size, block_size))

            pygame.display.update()
            count += 1
        pygame.quit()
        
if __name__ == "__main__":
    Game = Tetris(10, 20)
    Game.main()
        
