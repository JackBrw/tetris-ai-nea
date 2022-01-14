from typing import List

from pygame.draw import lines
from piece import *
from colours import *
from pygame import mixer
from ai import *
import pygame
import random

class Event: #Class that handles keys in for the AI
    type = None
    key = None

    def __init__(self, type, key):
        self.type = type
        self.key = key
        
class Tetris:
    def __init__(self, width, height, ai) -> None: #initialiser
        self.height = height
        self.width = width
        self.positions = {}
        self.grid = []
        self.current_piece: Piece = None
        self.level = 0
        self.pieces = []
        self.new_target = True
        self.bot = AI()
        self.current_piece: Piece = None
        self.score = 0
        self.lines_cleared = 0
        self.count = 0
        if ai: self.state = "ai"
        else: self.state = "play"
            
        
    def create_grid(self):
        self.grid = [[0 for _ in range(self.height)] for _ in range(self.width)]
        for x in range(len(self.grid)):
            for y in range(len(self.grid[x])):
                if (x, y) in self.positions:
                    self.grid[x][y] = self.positions[(x, y)]
                if self.current_piece != None:
                    for i in self.current_piece.get():
                        if i == (x, y):
                            self.grid[x][y] = self.current_piece.colour
    
    def detectCollision(self):
        values = self.current_piece.get()
        collision = False
        for block in values:
            a, b = block
            if a > self.width-1 or a < 0 or b > self.height-1 or block in self.positions:
                collision = True           
        return collision
    
    def draw_grid(self, win, buffer, block_size):
        for x in range(self.width): #draw the grid
            for y in range(self.height):
                colour = intToColour[self.grid[x][y]]
                pygame.draw.rect(win, colour,((buffer + x*block_size), (buffer + y*block_size), block_size, block_size))
                
        for i in range(1, self.height): #horizontal lines
            pygame.draw.line(win, (192, 192, 192), ((buffer), (buffer + i*block_size)), ((buffer + self.width * block_size), (buffer + i* block_size)))
        
        for i in range(1, self.width): #vertical lines
            pygame.draw.line(win, (192, 192, 192), ((buffer + i*block_size), (buffer)), ((buffer + i*block_size), (buffer + self.height * block_size)))
        pygame.display.update()    
        
        self.draw_next_piece(win, buffer, block_size)
        
    def draw_next_piece(self, win, buffer, block_size):
        if len(self.pieces) == 0:
            self.pieces = self.gen_pieces()
        next_piece = Piece(self.pieces[0], (0,0)) 
        blocks = next_piece.get()
        for x in range(0, 4):
            for y in range(0, 4):
                isBlock = False
                for block in blocks:
                    if block == (x, y):
                        isBlock = True
                if isBlock: colour = intToColour[next_piece.colour]
                else: colour = (117, 97, 113)
                pygame.draw.rect(win, colour, ((2*buffer + self.width *block_size + x*block_size, buffer + y*block_size), (2*buffer + self.width *block_size + (x+1)*block_size, buffer + (y+1)*block_size)))
        pygame.draw.rect(win, (117, 97, 113), ((2*buffer+self.width*block_size, buffer + 4*block_size), (self.s_width, buffer+8*block_size )))
        
    def freeze_piece(self):
        for block in self.current_piece.get():
            self.positions[block] = self.current_piece.colour
        if len(self.pieces) != 0:
            self.current_piece = Piece(self.pieces[0], (self.width/2-2, -2))
            del self.pieces[0]
        else:
            self.pieces = self.gen_pieces()
            self.current_piece = Piece(self.pieces[0], (self.width/2-2, -2))  
            del self.pieces[0]
        self.new_target = True
      
    def clear_and_check(self):
        lines_cleared = 0
        for y in range(self.height):
            count = 0
            for x in range(self.width):
                if (x, y) in self.positions:
                    count += 1
            if count == self.width:
                lines_cleared += 1
                for c in range(self.width):
                    self.positions.pop((c, y))
                for b in range(y-1, 0, -1):
                    for a in range(self.width):
                        if (a, b) in self.positions:
                            colour = self.positions[(a, b)]
                            self.positions.pop((a, b))
                            self.positions[(a, b+1)] = colour
                            
        self.lines_cleared += lines_cleared
        multiplier = self.level + 1
        if lines_cleared >= 1:
            line_clear = mixer.Sound('clear.wav')
            mixer.Sound.play(line_clear)
        if lines_cleared == 1: self.score += multiplier*40
        elif lines_cleared == 2: self.score += multiplier *100
        elif lines_cleared == 3: self.score += multiplier*300
        elif lines_cleared == 4: self.score += multiplier*1200
        
    def gen_pieces(self):
        tempList = list(range(7))
        random.shuffle(tempList)
        return tempList      
                            
    def check_lose(self):
        
        lost = False
        for x in range(self.width):
            if (x, 0) in self.positions:
                lost = True
        
        return lost

    def is_over(self, rect, pos): #input rectangle and mouse position
        return True if rect.collidepoint(pos[0], pos[1]) else False
    
    def run(self):
        level = self.lines_cleared // 10
        self.create_grid()
        self.level = self.lines_cleared // 10
        if len(self.pieces) == 0:
            self.pieces = self.gen_pieces()
            
        if self.current_piece == None:
            self.current_piece = Piece(self.pieces[0], (self.width/2-2, -2))
            del self.pieces[0]
            
        if self.state == "ai":
            botEvents = self.bot.proc(self.grid, self.current_piece, self.positions, self.width, self.height, self.new_target)
            self.new_target = False
        else:
            botEvents = []
            
        for event in pygame.event.get() + botEvents:
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()
                    
            if self.state == "play" or self.state == "ai":    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.current_piece.down()
                        if self.detectCollision() == True:
                            self.current_piece.up()
                            self.freeze_piece()
                            self.score += 2
                            
                    if event.key == pygame.K_LEFT:
                        self.current_piece.left()
                        if self.detectCollision() == True:
                            self.current_piece.right()
                            
                    if event.key == pygame.K_RIGHT:
                        self.current_piece.right()
                        if self.detectCollision() == True:
                            self.current_piece.left()
                            
                    if event.key == pygame.K_UP:
                        self.current_piece.rotate()
                        if self.detectCollision() == True:
                            for _ in range(3):
                                self.current_piece.rotate()
                                
                    if event.key == pygame.K_SPACE:
                        while not(self.detectCollision()):
                            self.current_piece.down()
                        self.current_piece.up()
                        self.freeze_piece()
                        self.score += 2
        if self.state == "play" or self.state == "ai":
            if self.state == "ai":
                level = 10
            if self.count >= 12 - level:
                if self.current_piece != None: self.current_piece.down()

                if self.detectCollision() == True:
                    self.current_piece.up()
                    self.freeze_piece()   
                    self.score += 2  
                self.count = 0                  
            self.count += 1
            self.clear_and_check()
            end = self.check_lose()
            if end:
                self.state = "quit"