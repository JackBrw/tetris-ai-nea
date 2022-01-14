from typing import Tuple

from numpy import block
from piece import *
from tetris import *
from ai import *
from colours import *
import pygame, os, ctypes, sys, math

#*SETUP VARIABLES
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)
state = "menu"
pygame.init()
win = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
if sys.platform == "win32":
    HWND = pygame.display.get_wm_info()['window']
    SW_MAXIMIZE = 3
    ctypes.windll.user32.ShowWindow(HWND, SW_MAXIMIZE)
win.fill(intToColour[8])
screen_width, screen_height = pygame.display.get_surface().get_size()
clock = pygame.time.Clock()
pygame.display.set_caption("Tetris")

#*FONTS BELOW
main_font = pygame.font.SysFont("Calibri", 25, True, False)

def draw_menu(win):
    
    #draws the 'Watch AI' button
    ai_text = main_font.render(f"Watch AI", True, intToColour[10])
    ai_rect= ai_text.get_rect(center=(screen_width/2, screen_height/2))
    ai_but_rect = pygame.Rect(screen_width/2 - 70, screen_height/2 - 30, 140, 60)
    pygame.draw.rect(win, intToColour[9], ai_but_rect)
    win.blit(ai_text, ai_rect)
    
    #draws the 'Play Game' button
    play_text = main_font.render(f"Play", True, intToColour[10])
    play_rect = play_text.get_rect(center=(screen_width/2, screen_height/2 - 90))
    play_but_rect = pygame.Rect(screen_width/2 - 70, screen_height/2 - 120, 140, 60)
    pygame.draw.rect(win, intToColour[9], play_but_rect)
    win.blit(play_text, play_rect)
    
    #draws the 'Watch Game' button
    train_text = main_font.render(f"Train AI", True, intToColour[10])
    train_rect = train_text.get_rect(center=(screen_width/2, screen_height/2 + 90))
    train_but_rect = pygame.Rect(screen_width/2 - 70, screen_height/2 + 60, 140, 60)
    pygame.draw.rect(win, intToColour[9], train_but_rect)
    win.blit(train_text, train_rect)
    
    return (play_but_rect, ai_but_rect, train_but_rect)
    
def is_over(rect, pos): #input rectangle and mouse position
    return True if rect.collidepoint(pos[0], pos[1]) else False #returns if the mouse is over the rectangle
    
def draw_tetris(tetris: Tetris, anchor: Tuple, win, block_size):
    a, b = anchor
    pygame.draw.rect(win, intToColour[9], pygame.Rect(a, b, 10*block_size, 20*block_size), 1)
    pygame.draw.rect(win, intToColour[8], pygame.Rect(a + 12*block_size, b, 4*block_size, 4*block_size))
    pygame.draw.rect(win, intToColour[9], pygame.Rect(a + 12*block_size, b, 4*block_size, 4*block_size), 1)

    for x in range(tetris.width): #draw the grid
        for y in range(tetris.height):
            colour = intToColour[tetris.grid[x][y]]
            pygame.draw.rect(win, colour,((a + x*block_size), (b + y*block_size), block_size, block_size))
            
    for i in range(1, tetris.height): #horizontal lines
        pygame.draw.line(win, intToColour[11], (a, b + i*block_size), (a + tetris.width*block_size, b + i*block_size))
        
    for i in range(1, tetris.width): #vertical lines
        pygame.draw.line(win, intToColour[11], (a + i*block_size, b), (a + i*block_size, b + tetris.height*block_size))
        
    #draw the next piece
    next_piece: Piece = None
    a1 = a + 12*block_size
    b1 = b
    if len(tetris.pieces) > 0:
        next_piece = Piece(tetris.pieces[0], (0,0))
    for y in range(4):
        for x in range(4):
            if next_piece != None:
                if next_piece.matrix[x][y] != 0:
                    val = 1
                    if next_piece.typeVal == 0 or next_piece.typeVal == 3 or next_piece.typeVal == 2: val = 0
                    pygame.draw.rect(win, intToColour[next_piece.colour], (a1 + (x+val)*block_size, b1 + y*block_size, block_size, block_size))
    
    score_font = pygame.font.SysFont("Calibri", block_size, True, False)
    score_text = score_font.render(f"Score: {tetris.score}", True, intToColour[11])
    score_rect = score_text.get_rect(center=(a1+2*block_size, b1+6*block_size))
    pygame.draw.rect(win, intToColour[8], score_rect)
    win.blit(score_text, score_rect)
games = []    
while __name__ == "__main__":
    
    #get updated values for inputs etc.
    mouse = pygame.mouse.get_pos()
    
    #all controls for the menu
    if state == "menu":
        play_but, ai_but, train_but = draw_menu(win)
        
        #gets user inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if is_over(play_but, mouse) or  is_over(ai_but, mouse): 
                    if is_over(play_but, mouse):state = "play"
                    else: state = "ai"
                    #create the tetris
                    isAi = is_over(ai_but, mouse)
                    games.append(Tetris(10, 20, isAi))
                    
                if is_over(train_but, mouse): 
                    state = "train"
                    
                    #re-size the screen
                    for _ in range(8):
                        games.append(Tetris(10, 20, True))
                pygame.draw.rect(win, intToColour[8], (0, 0, screen_width, screen_height))
                
    if state == "play" or state == "ai":
        for game in games: game.run()
        draw_tetris(games[0], (560, 50), win, 35)
        for game in games:
            if game.state != state:
                quit()
                
    if state == "train":
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         pygame.display.quit()
        #         quit()
        for i in range (len(games)): 
            if games[i].state == "ai":
                games[i].run()
            row = 450
            if i % 2 == 1: 
                row = 50
                column = (i-1)*200+50
            else:
                column = i*200+50
            draw_tetris(games[i], (column, row), win, 15)
        
    pygame.display.update()
    clock.tick(30)
