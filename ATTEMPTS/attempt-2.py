import pygame, sys, math
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
    def __init__(self, typeVal) -> None: #initialiser, converts the array of numbers into a 4x4 matrix
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

    def get(self): #get the value of the matrix
        return self.matrix

    def rotate(self): #rotate the matrix
        tempMat = self.matrix
        tempMat = np.transpose(tempMat)
        tempMat = np.flip(tempMat, 1)
        self.matrix = tempMat
        
    def position(self): #WIP
        pass
    
class Tetris:
    def __init__(self, width, height) -> None:
        self.__height = height
        self.__width = width
        self.__positions = {}
        self.__grid = []
        
    def create_grid(self, positions: dict) -> list: #creates the grid
        grid = [[(0, 0, 0) for x in range(self.__width)] for y in range(self.__height)]
        for x in range(len(grid)):
            for y in range(len(grid[x])):
                if (x, y) in positions:
                    grid[x][y] = positions[(x, y)]
        return grid
    
    def set_grid(self, positions: dict): #sets the grid to the base values (mainly for debugging)
        for x in range(0, self.__height - 1):
            for y in range(0, self.__width - 1):
                positions[(x, y)] = colour["white"]
        return positions
    
    def generate_piece(self, val):
        return Piece(val)
    
    def main(self):
        pass
        
