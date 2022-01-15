from typing import Tuple
from piece import *
from tetris import *
from ai import *
from colours import *
import pygame, os, ctypes, sys

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
quit_font = pygame.font.SysFont("Calibri", 100, True, False)
return_font = pygame.font.SysFont("Calibri", 60, True, False)

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
    a1 = a + 13*block_size
    b1 = b
    pygame.draw.rect(win, intToColour[8], pygame.Rect(a1, b, 4*block_size, 4*block_size))
    pygame.draw.rect(win, intToColour[9], pygame.Rect(a1, b, 4*block_size, 4*block_size), 1)
    if len(tetris.pieces) > 0:
        next_piece = Piece(tetris.pieces[0], (0,0))
    for y in range(4):
        for x in range(4):
            if next_piece != None:
                if next_piece.matrix[x][y] != 0:
                    val = 1
                    if next_piece.typeVal == 0 or next_piece.typeVal == 3 or next_piece.typeVal == 2: val = 0
                    pygame.draw.rect(win, intToColour[next_piece.colour], (a1 + (x+val)*block_size, b1 + y*block_size, block_size, block_size))
    
    
    pygame.draw.rect(win, intToColour[8], (a1 - 2*block_size, b1 + 4*block_size + 5, screen_width - (a1 - 2*block_size), screen_height - (b1 + 4*block_size + 5)))
    info_font = pygame.font.SysFont("Calibri", block_size, True, False)
    
    #draw the score
    score_text = info_font.render(f"Score: {tetris.score}", True, intToColour[11])
    score_rect = score_text.get_rect(center=(a1+2*block_size, b1+7*block_size))
    pygame.draw.rect(win, intToColour[8], score_rect)
    win.blit(score_text, score_rect)
    
    #draw the lines cleared
    lines_text = info_font.render(f"Lines: {tetris.lines_cleared}", True, intToColour[11])
    lines_rect = lines_text.get_rect(center=(a1+2*block_size, b1+8*block_size))
    pygame.draw.rect(win, intToColour[8], lines_rect)
    win.blit(lines_text, lines_rect)
    
    #draw the level
    level_text = info_font.render(f"Level: {tetris.level}", True, intToColour[11])
    level_rect = level_text.get_rect(center=(a1+2*block_size, b1+9*block_size))
    pygame.draw.rect(win, intToColour[8], level_rect)
    win.blit(level_text, level_rect)
    
    #draw weights if AI
    if tetris.state == "ai":
        weightList = list(tetris.weights)
        for i in range(len(tetris.weights)):
            calculated, weight = list(tetris.weights.items())[i]
            weight_text = info_font.render(f"{calculated}: {weight}", True, intToColour[11])
            weight_rect = weight_text.get_rect(center=(a1+2*block_size, b1+(13+i)*block_size))
            pygame.draw.rect(win, intToColour[8], weight_rect)
            win.blit(weight_text, weight_rect)
            
games = []   
gamesRunning = [] 
while __name__ == "__main__":
    
    #get updated values for inputs etc.
    mouse = pygame.mouse.get_pos()
    
    #all controls for the menu
    if state == "menu":
        games = []
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
                    for _ in range(6):
                        games.append(Tetris(10, 20, True))
                        gamesRunning.append(True)
                pygame.draw.rect(win, intToColour[8], (0, 0, screen_width, screen_height))
                
    if state == "play" or state == "ai":
        
        #run the game
        for game in games: game.run()
        
        #draw the game
        draw_tetris(games[0], (560, 50), win, 35)
        
        #check if lost
        for game in games:
            if game.state == "quit":
                state = game.state
                pygame.draw.rect(win, intToColour[8], (0, 0, screen_width, screen_height))
                
    if state == "train":
        
        #run and draw the games
        for i in range (len(games)): 
            if games[i].state == "ai":
                games[i].run()
            else:
                gamesRunning[i] = False
            row = 450
            if i % 2 == 1: 
                row = 50
                column = (i-1)*200+50
            else:
                column = i*200+50
                
            if gamesRunning[i]:
                draw_tetris(games[i], (column, row), win, 15)
            else:
                pygame.draw.rect(win, intToColour[9], (column, row, 15*games[i].width, 15*games[i].height))
                
            #reset all games and run the genetic algorithm to 'evolve' the games
            if not any(gamesRunning):
                for x in range(len(games)):
                    games[x].restart()
                    gamesRunning[x] = True
            
    if state == "quit":
            
            #draw you lost message
            quit_text = quit_font.render(f"You Lost! Score: {games[0].score}", True, intToColour[10])
            quit_rect = quit_text.get_rect(center=(screen_width/2, screen_height/2 - 50))
            pygame.draw.rect(win, intToColour[8], quit_rect)
            win.blit(quit_text, quit_rect)
            
            #draws the 'Return to Menu' button
            menu_text = return_font.render(f"Return to Menu", True, intToColour[10])
            menu_rect = menu_text.get_rect(center=(screen_width/2, screen_height/2 + 90))
            menu_but_rect = pygame.Rect(screen_width/2 - 200, screen_height/2 + 45, 400, 90)
            pygame.draw.rect(win, intToColour[9], menu_but_rect)
            win.blit(menu_text, menu_rect)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    quit()
                    
                #gets the button press for return to menu
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if is_over(menu_but_rect, mouse):
                        state = "menu"
                        pygame.draw.rect(win, intToColour[8], (0, 0, screen_width, screen_height))
        
    pygame.display.update()
    clock.tick(30)
