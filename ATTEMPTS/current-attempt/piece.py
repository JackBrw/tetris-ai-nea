import random as rd
from figures import *
import numpy as np

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
        self.colour = 1
                    
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
        
    def up(self):
        a, b = self.anchor
        b -= 1
        self.anchor = (a, b)