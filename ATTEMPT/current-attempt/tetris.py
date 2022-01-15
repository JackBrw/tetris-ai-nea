from turtle import speed
from typing import List

from pygame.draw import lines
from piece import *
from colours import *
from pygame import mixer
from ai import *
import pygame
import random

#Class that handles keys in for the AI
class Event: 
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
        self.weights = self.bot.weight
        if ai: self.state = "ai"
        else: self.state = "play"
            
    #reset the values and restart the game, only call on 'ai' mode
    def restart(self):
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
        self.weights = self.bot.weight
        self.state = "ai"
        
    #creates the grid
    def create_grid(self):
        
        #create an empty grid
        self.grid = [[0 for _ in range(self.height)] for _ in range(self.width)]
        
        #loop through the grid
        for x in range(len(self.grid)):
            for y in range(len(self.grid[x])):
                
                #if the cell is in the position dictionary, change the colour of the grid
                if (x, y) in self.positions:
                    self.grid[x][y] = self.positions[(x, y)]
                    
                #put the piece in the grid
                if self.current_piece != None:
                    for i in self.current_piece.get():
                        if i == (x, y):
                            self.grid[x][y] = self.current_piece.colour
    
    #detect a collision between the current piece and anywhere
    def detectCollision(self):
        
        #get the position of each 'block' in the current piece
        values = self.current_piece.get()
        collision = False
        for block in values:
            a, b = block
            
            #check if block is out of bounds or touching another block
            if a > self.width-1 or a < 0 or b > self.height-1 or block in self.positions:
                collision = True           
        return collision
        
    #'freeze' and change the curent piece
    def freeze_piece(self):
        
        #put the current piece into the positions dictionary
        for block in self.current_piece.get():
            self.positions[block] = self.current_piece.colour
            
        #change the current piece if possible
        if len(self.pieces) != 0:
            self.current_piece = Piece(self.pieces[0], (self.width/2-2, -2))
            del self.pieces[0]
        
        #generate the next set of pieces if needed and change the current piece
        else:
            self.pieces = self.gen_pieces()
            self.current_piece = Piece(self.pieces[0], (self.width/2-2, -2))  
            del self.pieces[0]
            
        #tell the AI class it needs to find the target for the new piece
        self.new_target = True
      
    #check if lines need to be cleared, and clear if they do
    def clear_and_check(self):
        lines_cleared = 0
        
        #loop through the grid(via the positions library)
        for y in range(self.height):
            count = 0
            for x in range(self.width):
                if (x, y) in self.positions:
                    count += 1
                    
            #if there is a full line, clear it
            if count == self.width:
                lines_cleared += 1
                
                #remove each block from the line that is being cleared
                for c in range(self.width):
                    self.positions.pop((c, y))
                    
                #move every piece above the cleared line down
                for b in range(y-1, 0, -1):
                    for a in range(self.width):
                        if (a, b) in self.positions:
                            colour = self.positions[(a, b)]
                            self.positions.pop((a, b))
                            self.positions[(a, b+1)] = colour
                  
        #increase the number of lines cleared          
        self.lines_cleared += lines_cleared
        
        #add the correct score to the current score
        multiplier = self.level + 1
        if lines_cleared == 1: self.score += multiplier*40
        elif lines_cleared == 2: self.score += multiplier *100
        elif lines_cleared == 3: self.score += multiplier*300
        elif lines_cleared == 4: self.score += multiplier*1200
        
    #generate the next 7 pieces to appear
    def gen_pieces(self):
        tempList = list(range(7))
        random.shuffle(tempList)
        return tempList      
                  
    #check if the game has been lost          
    def check_lose(self):
        
        lost = False
        for x in range(self.width):
            if (x, 0) in self.positions:
                lost = True
        
        return lost

    #check if the mouse is over a pygame rectangle
    def is_over(self, rect, pos): #input rectangle and mouse position
        return True if rect.collidepoint(pos[0], pos[1]) else False
    
    #run the main game
    def run(self):
        
        #generate the grid based on the positions
        self.create_grid()
        
        #calculate the current level
        self.level = self.lines_cleared // 10
        
        #generate the next pieces if needed
        if len(self.pieces) == 0:
            self.pieces = self.gen_pieces()
            
        #generate current piece if needed
        if self.current_piece == None:
            self.current_piece = Piece(self.pieces[0], (self.width/2-2, -2))
            del self.pieces[0]
            
        #find the next move to make if the AI is running
        if self.state == "ai":
            botEvents = self.bot.proc(self.grid, self.current_piece, self.positions, self.width, self.height, self.new_target)
            self.new_target = False
        else:
            botEvents = []
            
        #cycle through each pygame event
        for event in pygame.event.get() + botEvents:
            
            #quit if the windows quit button is pressed
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()
                    
            if self.state == "play" or self.state == "ai":    
                if event.type == pygame.KEYDOWN:
                    
                    #move the piece down if down arrow is pressed
                    if event.key == pygame.K_DOWN:
                        self.current_piece.down()
                        if self.detectCollision() == True:
                            self.current_piece.up()
                            self.freeze_piece()
                            self.score += 2
                            
                    #move the piece left if left arrow is pressed
                    if event.key == pygame.K_LEFT:
                        self.current_piece.left()
                        if self.detectCollision() == True:
                            self.current_piece.right()
                            
                    #move the piece right if right arrow is pressed
                    if event.key == pygame.K_RIGHT:
                        self.current_piece.right()
                        if self.detectCollision() == True:
                            self.current_piece.left()
                            
                    #rotate the piece if up arrow is pressed
                    if event.key == pygame.K_UP:
                        self.current_piece.rotate()
                        if self.detectCollision() == True:
                            for _ in range(3):
                                self.current_piece.rotate()
                                
                    #move the piece all the way to the bottom
                    if event.key == pygame.K_SPACE:
                        while not(self.detectCollision()):
                            self.current_piece.down()
                        self.current_piece.up()
                        self.freeze_piece()
                        self.score += 2
                        
        if self.state == "play" or self.state == "ai":
            
            #make the speed the ai game moves at constant
            if self.state == "ai":
                speed = 10
                
            #make the speed correlate to the level
            if self.level > 10:
                speed = 10
            else:
                speed = self.level
            if self.count >= 12 - speed:
                
                #move the piece down at the set interval
                if self.current_piece != None: self.current_piece.down()

                #detect a collision
                if self.detectCollision() == True:
                    self.current_piece.up()
                    self.freeze_piece()   
                    self.score += 2  
                self.count = 0                  
            self.count += 1
            
            #check if any lines need to be cleared
            self.clear_and_check()
            
            #check if game has been lost
            end = self.check_lose()
            if end:
                self.state = "quit"