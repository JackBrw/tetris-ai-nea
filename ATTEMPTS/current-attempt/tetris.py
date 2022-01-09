from typing import List

from pygame.draw import lines
from piece import *
from colours import *
from pygame import mixer
import ai
import pygame
import random

class Tetris:
    def __init__(self, width, height, s_width, s_height) -> None: #initialiser
        self.height = height
        self.width = width
        self.s_width = s_width
        self.s_height = s_height
        self.positions = {}
        self.grid = []
        self.current_piece: Piece = None
        self.level = 0
        self.pieces = []
        
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
            if a > self.width - 1 or a < 0 or b > self.height - 1:
                collision = True
            elif block in self.positions:
                collision = True
                
        return collision
    
    def draw_grid(self, win, buffer, block_size):
        for x in range(self.width): #draw the grid from the dictionary
            for y in range(self.height):
                colour = intToColour[self.grid[x][y]]
                pygame.draw.rect(win, colour,((buffer + x*block_size), (buffer + y*block_size), block_size, block_size))
                
        for i in range(1, self.height): #horizontal lines
            pygame.draw.line(win, (192, 192, 192), ((buffer), (buffer + i*block_size)), ((buffer + self.width * block_size), (buffer + i* block_size)))
        
        for i in range(1, self.width): #vertical lines
            pygame.draw.line(win, (192, 192, 192), ((buffer + i*block_size), (buffer)), ((buffer + i*block_size), (buffer + self.height * block_size)))
        pygame.display.update()    
        
    
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
        
        return not(lost)
        
        
    
    def run(self):
        run = True
        pygame.init()
        s_width = self.s_width
        s_height = self.s_height
        win = pygame.display.set_mode((s_width, s_height))
        buffer = s_width / 8 - ((s_width / 8) % 10)
        block_size = (s_height - 2*buffer)/ self.height
        
        font = pygame.font.SysFont("Calibri", 25, True, False)
        pygame.display.set_caption("Tetris")
        win.fill((117, 97, 113))
        count = 0
        self.current_piece: Piece = None
        self.score = 0
        self.lines_cleared = 0
        
        clock = pygame.time.Clock()
        fps = 100
        level = 1
        #?MUSIC
        mixer.init()
        mixer.music.load('music.mp3')
        mixer.music.set_volume(0.7)
        mixer.music.play(-1)
        
        while run:
            # for each level falling speed increases by 0.05 secs per block
            self.level = self.lines_cleared // 10
            self.create_grid()
            if len(self.pieces) == 0:
                self.pieces = self.gen_pieces()
                
            if self.current_piece == None:
                self.current_piece = Piece(self.pieces[0], (self.width/2-2, -2))
                del self.pieces[0]
            
            for event in list(pygame.event.get()):
                if event.type == pygame.QUIT:
                    run = False
                    pygame.display.quit()
                    quit()
                    
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
                        
            if count >= 50 - 5*level:
                if self.current_piece != None: self.current_piece.down()

                if self.detectCollision() == True:
                    self.current_piece.up()
                    self.freeze_piece()   
                    self.score += 2  
                count = 0                  
            
            text = font.render(f"Score: {self.score}  ||  Level: {self.level}  ||  Cleared: {self.lines_cleared}", True, intToColour[7])
            pygame.draw.rect(win, (117, 97, 113), ((0, 0), (self.s_width, buffer)))
            win.blit(text, (0, 0))
            self.draw_grid(win, buffer, block_size)
            pygame.display.flip()
            count += 1
            self.clear_and_check()
            run = self.check_lose()
            
            clock.tick(fps)
    
        