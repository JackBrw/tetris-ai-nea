import pygame, sys, math
from pygame.locals import *
import numpy as np
import random as rd

colour = {
    "black":(0, 0, 0),
    "white":(255, 255, 255),
    "red":(255, 0, 0),
    "green":(0, 255, 0),
    "blue":(0, 0, 255)
}

class Piece: # * The class that holds a matrix of the piece
    def __init__(self, typeVal) -> None:
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
        return self.matrix

    def rotate(self):
        tempMat = self.matrix
        tempMat = np.transpose(tempMat)
        tempMat = np.flip(tempMat, 1)
        self.matrix = tempMat

def figures(figure): # * holds the 7 grid positions for the pieces
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

class Tetris: # TODO: make the grid and the ability for the pieces to move down the grid
    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.grid = []
        self.state = "start"
    
    def create_grid(self, locked_positions: dict): # * makes the grid using a dictionary of locked positions
        grid = [[(0, 0, 0) for x in range(self.width)] for y in range(self.height)]
        for x in range(len(grid)):
            for y in range(len(grid[x])):
                if (x, y) in locked_positions:
                    grid[x][y] = locked_positions[(x, y)]
        return grid
    
    def set_grid(self, positions: dict):
        for x in range(0, self.height - 1):
            for y in range(0, self.width - 1):
                positions[(x, y)] = colour["white"]
        return positions
    def generate_piece(self):
        return Piece(-1)
    
class Game:
    def __init__(self, width, height) -> None:
        self.height = height
        self.width = width
        self.Tetro = Tetris(height, width)
        self.positions = {}
    
    def main(self):
        pygame.init()
        run = True
        s_width = 500
        s_height = 600
        buffer = s_width / 8 - ((s_width / 8) % 10)
        win = pygame.display.set_mode((s_width, s_height))
        block_size = (s_height - 2*buffer)/ self.height
        
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.display.quit()
                    quit()

            self.positions = self.Tetro.set_grid(self.positions)
            grid = self.Tetro.create_grid(self.positions)
            
            for y in range(0, self.height):
                for x in range (0, self.width):
                    pygame.draw.rect(win, grid[x][y] , ((buffer + x*block_size), (buffer + y*block_size), block_size, block_size))
                      
            pygame.display.update()
        pygame.quit()
        
if __name__ == "__main__":
    Play = Game(10, 20)
    Play.main()
