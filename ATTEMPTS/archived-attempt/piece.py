import random as rd
import numpy as np

def figures(x): #*returns the specific figure
    figures = {
        0:(1, 5, 9, 13), #I piece [0]
        1:(1, 5, 8, 9), #J piece [1]
        2:(1, 5, 9, 10), #L piece [2]
        3:(5, 6, 9, 10), #O piece [3]
        4:(0, 4, 5, 9), #S piece [4]
        5:(0, 4, 5, 8), #T piece [5]
        6:(1, 4, 5, 8) #Z piece [6]
    }
    return figures[x]

class Block:
    def __init__(self, coord, colour, piece) -> None:
        self.coord = coord #coordinate of piece
        self.colour = colour #colour of the piece
        self.piece = piece #whether it is part of a piece or not
        
    #*GETTERS AND SETTERS BELOW    
    def set_coord(self, new):
        self.coord = new
        
    def get_coord(self):
        return self.coord
    
    def get_colour(self):
        return self.colour
    
    def get_state(self):
        return self.piece
    
    def move(self, arg): #moves the block down, left or right
        a, b = self.coord
        if arg == "left":
            b -= 1
        elif arg == "right":
            b += 1
        elif arg == "down":
            a += 1
        self.set_coord((a, b))
        
class Piece:
    def __init__(self, val, colour, anchor) -> None:
        self.colour = colour
        if val != -1:
            self.val = val
        else:
            val = rd.randint(0, 6)
            self.val = val
        self.shape = figures(val)
        self.anchor = anchor 
        self.blocks: list(Block) = self.construct()
        self.matrix = self.build_matrix()
        
    def construct(self) -> list:
        true_positions = []
        constructs = []
        a, b = self.anchor
        for y in range(4):
            for x in range(4):
                for z in range(len(self.shape)):
                    if (x + y*4) == self.shape[z]:
                        true_positions.append((a+x, b+y))
                        
        for i in range(len(true_positions)):
            constructs.append(Block(true_positions[i], self.colour, True))
        return constructs
    
    def build_matrix(self):
        matrix = np.zeros((4, 4), dtype=int)
        for i in range(4):
            a, b = self.blocks[i].get_coord()
            x, y = self.anchor
            matrix[a - x][b - y] = i + 1
        return matrix
    
    def rotate(self):
        squareorline = (self.val == 0 or self.val == 3)
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
                   
        a, b = self.anchor
        for i in range(len(self.blocks)):
            j, k = (0, 0)
            for x in range(4):
                for y in range(4):
                    if self.matrix[x, y] == i + 1:
                        j = x
                        k = y
            self.blocks[i].set_coord((a+j, b+k))
        
                   
    def get_block(self):
        list = []
        for i in range(len(self.blocks)):
            list.append(self.blocks[i])
        return list
    
    def move(self, arg):
        a, b = self.anchor
        if arg == "left":
            b -= 1
        elif arg == "right":
            b += 1
        elif arg == "down":
            a += 1
        self.anchor = (a, b)
        for i in range(len(self.blocks)):
            self.blocks[i].move(arg)