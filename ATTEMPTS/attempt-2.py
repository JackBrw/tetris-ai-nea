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
    "blue":(0, 0, 255),
    "l_blue":(186, 213, 245),
    "d_blue":(68, 66, 146)
}

def figures(figure): # holds the 7 grid positions for the pieces
    figures = (
        (1, 5, 9, 13), #I piece [0]
        (1, 5, 8, 9), #J piece [1]
        (1, 5, 9, 10), #L piece [2]
        (5, 6, 9, 10), #O piece [3]
        (0, 4, 5, 9), #S piece [4]
        (0, 4, 5, 8), #T piece [5]
        (1, 4, 5, 8) #Z piece [6]
    )
    return(figures[figure])


class Piece: # * The class that holds a matrix of the piece
    def __init__(self, typeVal, anchor) -> None: #initialiser, converts the array of numbers into a 4x4 matrix
        if typeVal == -1:
            typeVal = rd.randint(0, 6)
            self.typeVal = typeVal
        else:
            self.typeVal = typeVal
        self.moving = True
        self.anchor = anchor
        self.values = figures(typeVal)
        self.matrix = np.zeros((4, 4), dtype=int)
        a, b, c, d = self.values
        for x in range(0, 4): #1, 5, 9, 13
            for y in range(0, 4):
                if (x + y*4) == a:
                    self.matrix[x, y] = 1
                if (x + y*4) == b:
                    self.matrix[x, y] = 1
                if (x + y*4) == c:
                    self.matrix[x, y] = 1
                if (x + y*4) == d:
                    self.matrix[x, y] = 1
                    
    def get(self):
        return self.position()
                    
    def rotate(self): #rotate the matrix
        squareorline = (self.typeVal == 0 or self.typeVal == 3)
        if squareorline == True:
            tempMat = self.matrix
            tempMat = np.transpose(tempMat)
            tempMat = np.flip(tempMat, 1)
            self.matrix = tempMat
        else:
            tempMat = np.zeros((3, 3), dtype=int)
            for x in range(0, 3):
                for y in range(0, 3):
                    tempMat[x, y] = self.matrix[x, y]
            tempMat = np.transpose(tempMat)
            tempMat = np.flip(tempMat, 1)
            for x in range(0, 3):
                for y in range(0, 3):
                    self.matrix[x, y] = tempMat[x, y]
        
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
        
    def left(self):
        a, b = self.anchor
        a -= 1
        self.anchor = (a, b)
        
    def right(self):
        a, b = self.anchor
        a += 1
        self.anchor = (a, b)
    
    def bounds(self):
        a, b = self.anchor
        num = 0
        for y in range(3, 0, -1):
            if self.matrix[0][y] == 1:
                if y >= num : num = y
            if self.matrix[1][y] == 1:
                if y >= num : num = y
            if self.matrix[2][y] == 1:
                if y >= num : num = y
            if self.matrix[3][y] == 1:
                if y >= num : num = y
        lower = num + b
        num = 3
        for x in range(0, 3):
            if self.matrix[x][0] == 1:
                if x <= num : num = x
            if self.matrix[x][1] == 1:
                if x <= num : num = x
            if self.matrix[x][2] == 1:
                if x <= num : num = x
            if self.matrix[x][3] == 1:
                if x <= num : num = x
        left = num + a
        
        num = 0
        for x in range(0, 3):
            if self.matrix[x][0] == 1:
                if x >= num : num = x
            if self.matrix[x][1] == 1:
                if x >= num : num = x
            if self.matrix[x][2] == 1:
                if x >= num : num = x
            if self.matrix[x][3] == 1:
                if x >= num : num = x
        right = num + a
        
        return [lower, left, right]
        
           
    
class Tetris:
    def __init__(self, width, height) -> None: #initialiser
        self.height = height
        self.width = width
        self.positions = {}
        self.grid = []
        self.current_piece = None
        
    def create_grid(self, positions: dict) -> list: #creates the grid i.e sets the colour values
        grid = [[colour["l_blue"] for _ in range(self.height)] for _ in range(self.width)]
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
            if piece.get()[x] in positions:
                del positions[piece.get()[x]]
        return positions
    
    def main(self):
        #* GAME INIT
        run = True
        pygame.init()
        s_width = 500
        s_height = 600
        win = pygame.display.set_mode((s_width, s_height))
        buffer = s_width / 8 - ((s_width / 8) % 10)
        block_size = (s_height - 2*buffer)/ self.height
        #* OTHER
        pygame.display.set_caption("Tetris")
        win.fill(colour["d_blue"])
        count = 0
        self.current_piece = Piece(2, (3, -3))
        
        
        while run == True:
            self.positions = self.place_piece(self.current_piece, self.positions)
            self.grid = self.create_grid(self.positions)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.display.quit()
                    quit()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        if self.current_piece.bounds()[0] <= self.height - 1:
                            self.positions = self.remove_piece(self.current_piece, self.positions)
                            self.current_piece.down()
                            if self.current_piece.bounds()[0] >= self.height - 1:
                                self.positions = self.place_piece(self.current_piece, self.positions)
                                self.current_piece = Piece(-1, (3, -3))
                    
                    if event.key == pygame.K_LEFT:
                        if self.current_piece.bounds()[1] > 0:
                            self.positions = self.remove_piece(self.current_piece, self.positions)
                            self.current_piece.left()
                            
                    if event.key == pygame.K_RIGHT:
                        if self.current_piece.bounds()[2] < self.width - 1:
                            self.positions = self.remove_piece(self.current_piece, self.positions)
                            self.current_piece.right()
                            
                    if event.key == pygame.K_UP:
                        self.positions = self.remove_piece(self.current_piece, self.positions)
                        self.current_piece.rotate()
                        while self.current_piece.bounds()[1] < 0 : self.current_piece.right()
                        while self.current_piece.bounds()[2] > self.width - 1: self.current_piece.left()
                            
            if count > 300:
                if self.current_piece.bounds()[0] <= 19:
                    self.positions = self.remove_piece(self.current_piece, self.positions)
                    self.current_piece.down()
                    if self.current_piece.bounds()[0] >= 19:
                        self.positions = self.place_piece(self.current_piece, self.positions)
                        self.current_piece = Piece(-1, (3, -3))  
                count = 0                  
                        
                    
            for x in range(self.width): #draw the grid from the dictionary
                for y in range (self.height):
                    pygame.draw.rect(win, self.grid[x][y] , ((buffer + x*block_size), (buffer + y*block_size), block_size, block_size))

            pygame.display.update()
            count += 1
        pygame.quit()
        
if __name__ == "__main__":
    Game = Tetris(10, 20)
    Game.main()
        
