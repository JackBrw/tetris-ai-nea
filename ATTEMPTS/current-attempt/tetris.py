from piece import *
import pygame

class Tetris:
    def __init__(self, width, height) -> None: #initialiser
        self.height = height
        self.width = width
        self.positions = {}
        self.grid = []
        self.current_piece: Piece = None
        
    def create_grid(self):
        self.grid = [[0 for _ in range(self.height)] for _ in range(self.width)]
        for x in range(len(self.grid)):
            for y in range(len(self.grid[x])):
                if (x, y) in self.positions:
                    self.grid[x][y] = self.positions[(x, y)]
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
                if self.grid[x][y] == 0:
                    colour = (186, 213, 245)
                else:
                    colour = (255, 255, 255)
                pygame.draw.rect(win, colour,((buffer + x*block_size), (buffer + y*block_size), block_size, block_size))
    
    def freeze_piece(self):
        for block in self.current_piece.get():
            self.positions[block] = self.current_piece.colour
        self.current_piece = Piece(-1, (0,0))
    
    def main(self):
        run = True
        pygame.init()
        s_width = 500
        s_height = 600
        win = pygame.display.set_mode((s_width, s_height))
        buffer = s_width / 8 - ((s_width / 8) % 10)
        block_size = (s_height - 2*buffer)/ self.height
        
        pygame.display.set_caption("Tetris")
        win.fill((68, 66, 146))
        count = 0
        self.current_piece = Piece(-1, (0, 0))
        
        while run:
            self.create_grid()
            
            for event in pygame.event.get():
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
                            
            
            self.draw_grid(win, buffer, block_size)
            pygame.display.update()
           
t = Tetris(10, 20)     
t.main()
    
        