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
    
class Piece:
    def __init__(self, val, colour) -> None:
        self.colour = colour #colour of the piece
        self.val = val 
        self.shape = figures(val) #gets the shape of the piece
        self.matrix = np.zeros((4, 4), dtype=int)
        
    def construct(self):
        a, b, c, d = self.shape
        for x in range(0, 4): #1, 5, 9, 13
            for y in range(0, 4):
                if (x + y*4) == a:
                    self.matrix[x, y] = 1
                if (x + y*4) == b:
                    self.atrix[x, y] = 1
                if (x + y*4) == c:
                    self.matrix[x, y] = 1
                if (x + y*4) == d:
                    self.matrix[x, y] = 1
                    
    def true_positions(self) -> list:
        