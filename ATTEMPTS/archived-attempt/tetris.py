from piece import *
import pygame

class Tetris:
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height
    
    def create_grid(self, pieces):
        grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for piece in pieces.values(): #loops through each piece/block in the dictionary
            if isinstance(piece, Piece): #checks if it is a piece
                for block in piece.get_block(): #puts each block in the piece onto the grid
                    x, y = block.get_coord()
                    grid[x][y] = block.get_colour()
            elif isinstance(piece, Block): #checks if it is a block
                x, y = piece.get_coord() #puts the block into the grid
                grid[x][y] = piece.get_colour()
            
        return grid
    
    def draw_grid(self, win, grid, buffer, block_size):
        for x in range(self.height): #draw the grid from the dictionary
            for y in range(self.width):
                if grid[x][y] == 0:
                    colour = (0, 0, 0)
                else:
                    colour = (255, 255, 255)
                pygame.draw.rect(win, colour,((buffer + y*block_size), (buffer + x*block_size), block_size, block_size))
                
    def rotate(self, piece, grid):
        ghost_piece = piece
        ghost_piece.rotate()
        valid = False
        while valid == False:
            for block in ghost_piece.get_block():
                val = 0
                y, x = block.get_coord()
                if x < 0:
                    ghost_piece.move("right")
                    val += 1
                elif x > self.width - 1:
                    ghost_piece.move("left")
                    val += 1
            if val == 0: valid = True
        return ghost_piece
    
    def get_left(self, piece, grid):
        possible = True
        for block in piece.get_block():
            y, x = block.get_coord()
            if x <= 0:
                possible = False
        return possible
    
    def get_right(self, piece, grid):
        possible = True
        for block in piece.get_block():
            y, x = block.get_coord()
            if x >= self.width - 1:
                possible = False
        return possible
    
    def get_down(self, piece, grid):
        possible = True
        for block in piece.get_block():
            y, x = block.get_coord()
            if y >= self.height - 1:
                possible = False
                
        return possible
    
    def main(self):
        pygame.init()
        s_width = 500
        s_height = 600
        win = pygame.display.set_mode((s_width, s_height))
        buffer = s_width / 8 - ((s_width / 8) % 10)
        block_size = (s_height - 2*buffer)/ self.height
        win.fill((68, 66, 146))
        #!------------------------------
        
        current_piece = Piece(-1, 4, (3, 3))
        pieces = {}
        run = True
        next_id = 0
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.display.quit()
                    quit()
                    
                if event.type == pygame.KEYDOWN:
                    possible = True
                    if event.key == pygame.K_DOWN:
                        possible = self.get_down(current_piece, grid)
                        if possible:
                            current_piece.move("down")
                        else:
                            pieces[next_id] = current_piece
                            current_piece = Piece(-1, 2, (0, 0))
                            next_id += 1
                        
                    if event.key == pygame.K_LEFT:
                        possible = self.get_left(current_piece, grid)
                        if possible:
                            current_piece.move("left")
                        
                    if event.key == pygame.K_RIGHT:
                        possible = self.get_right(current_piece, grid)
                        if possible:
                            current_piece.move("right")
                            
                    if event.key == pygame.K_UP:
                        current_piece = self.rotate(current_piece, grid)
                        
                        
            pieces['c'] = current_piece
            grid = self.create_grid(pieces)
            self.draw_grid(win, grid, buffer, block_size)
            pygame.display.update()
        pygame.quit()
        
t = Tetris(10, 20)
t.main()
pass                