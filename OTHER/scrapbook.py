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