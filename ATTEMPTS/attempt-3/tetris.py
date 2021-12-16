from piece import *
import pygame

class Tetris:
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height
        
    def create_grid(self, pieces):
        grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for piece in pieces:
            if isinstance(pieces[piece], Piece):
                for i in range(len(pieces[piece].blocks)):
                    x, y = pieces[piece].blocks[i].get_coord()
                    grid[y][x] = pieces[piece].blocks[i].get_colour()
            elif isinstance(pieces[piece], Block):
                x, y = pieces[piece].get_coord()
                grid[y][x] = pieces[piece].get_colour()
                    
        return grid
    
    def draw_grid(self, win, grid, buffer, block_size):
            for y in range(self.height): #draw the grid from the dictionary
                for x in range(self.width):
                    if grid[y][x] == 0:
                        colour = (0, 0, 0)
                    else:
                        colour = (255, 255, 255)
                    pygame.draw.rect(win, colour,((buffer + x*block_size), (buffer + y*block_size), block_size, block_size))
                    
    def rotate(self, piece, grid):
        ghost_piece = piece
        ghost_piece.rotate()
        valid = False
        while valid == False:
            for block in ghost_piece.get_block():
                val = 0
                a, b = block.get_coord()
                if a < 0:
                    ghost_piece.move("right")
                    val += 1
                elif a > 9:
                    ghost_piece.move("left")
                    val += 1
            if val == 0: valid = True
        return ghost_piece

        
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
                        for block in current_piece.get_block():
                            a, b = block.get_coord()
                            if b >= 19:
                                possible = False
                        if possible:
                            current_piece.move("down")
                        else:
                            pieces[next_id] = current_piece
                            current_piece = Piece(-1, 2, (0, 0))
                            next_id += 1
                        
                    if event.key == pygame.K_LEFT:
                        for block in current_piece.get_block():
                            a, b = block.get_coord()
                            if a <= 0:
                                possible = False
                        if possible:
                            current_piece.move("left")
                        
                    if event.key == pygame.K_RIGHT:
                        for block in current_piece.get_block():
                            a, b = block.get_coord()
                            if a >= 9:
                               possible = False
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
pass