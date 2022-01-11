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
    def __init__(self, width, height, s_width, s_height, ai) -> None: #initialiser
        self.height = height
        self.width = width
        self.s_width = s_width
        self.s_height = s_height
        self.positions = {}
        self.grid = []
        self.current_piece: Piece = None
        self.level = 0
        self.pieces = []
        self.isAi = ai
        self.new = True
        
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
        for x in range(self.width): #draw the grid from the dictionary
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
        self.new = True
      
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

    def is_over(self, rect, pos): #input rectangle and mouse position
        return True if rect.collidepoint(pos[0], pos[1]) else False
    
    def run(self):
        state = "menu"
        run = True
        pygame.init()
        s_width = self.s_width
        s_height = self.s_height
        win = pygame.display.set_mode((s_width, s_height))
        buffer = s_width / 8 - ((s_width / 8) % 10)
        block_size = (s_height - 2*buffer)/ self.height
        
        score_font = pygame.font.SysFont("Calibri", 25, True, False)
        main_font = pygame.font.SysFont("Calibri", 25, True, False)
        pygame.display.set_caption("Tetris")
        win.fill((117, 97, 113))
        count = 0
        self.current_piece: Piece = None
        self.score = 0
        self.lines_cleared = 0
        
        clock = pygame.time.Clock()
        fps = 30
        level = 1
        
        #*MUSIC
        # mixer.init()
        # mixer.music.load('music.mp3')
        # mixer.music.set_volume(0.7)
        # mixer.music.play(-1)
        
        bot = AI()
        
        while run:
            # for each level falling speed increases by 0.05 secs per block
            mouse = pygame.mouse.get_pos()
            self.create_grid()
            self.level = self.lines_cleared // 10
            if len(self.pieces) == 0:
                self.pieces = self.gen_pieces()
                
            if self.current_piece == None:
                self.current_piece = Piece(self.pieces[0], (self.width/2-2, -2))
                del self.pieces[0]
                    
            if state == "menu":
                main_text = main_font.render(f"Play", True, intToColour[7])
                ai_text = main_font.render(f"AI", True, intToColour[7])
                main_rect = main_text.get_rect(center=(s_width/2, s_height/2-50))
                ai_rect = main_text.get_rect(center=(s_width/2+5, s_height/2+50))
                play_rect = pygame.Rect(s_width/2-40, s_height/2-80, 80, 60)
                aiBut_rect = pygame.Rect(s_width/2-40, s_height/2+20, 80, 60)
                pygame.draw.rect(win, intToColour[2], play_rect)
                pygame.draw.rect(win, intToColour[2], aiBut_rect)
                win.blit(main_text, main_rect)
                win.blit(ai_text, ai_rect)
                
            if state == "ai":
                botEvents = bot.proc(self.grid, self.current_piece, self.positions, self.width, self.height, self.new)
                self.new = False
            else:
                botEvents = []
                
            for event in pygame.event.get() + botEvents:
                if event.type == pygame.QUIT:
                    run = False
                    pygame.display.quit()
                    quit()
                if state == "menu":    
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.is_over(play_rect, mouse): state = "run"
                        if self.is_over(aiBut_rect, mouse): state = "ai"
                        pygame.draw.rect(win, (117, 97, 113), (0, 0, s_width, s_height))
                        
                if state == "run" or state == "ai":    
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
            if state == "run" or state == "ai":
                if count >= 12 - level:
                    if self.current_piece != None: self.current_piece.down()

                    if self.detectCollision() == True:
                        self.current_piece.up()
                        self.freeze_piece()   
                        self.score += 2  
                    count = 0                  
            
                text = score_font.render(f"Score: {self.score}  ||  Level: {self.level}  ||  Cleared: {self.lines_cleared}", True, intToColour[7])
                pygame.draw.rect(win, (117, 97, 113), ((0, 0), (self.s_width, buffer)))
                win.blit(text, (0, 0))
                self.draw_grid(win, buffer, block_size)
                count += 1
                self.clear_and_check()
                run = self.check_lose()
            
            pygame.display.update()
            clock.tick(fps)

        