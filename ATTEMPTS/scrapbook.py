for x in range(0, 3):
    for y in range(0, 3):
        if (y == 3 or x == 3) and squareorline == False:
            self.matrix[x, y] = 0
        else:
            self.matrix[x, y] = tempMat[x, y]
            

if count > 300:
    if self.current_piece.lower_bound() <= 19:
        self.positions = self.remove_piece(self.current_piece, self.positions)
        self.current_piece.down()
        if self.current_piece.lower_bound() >= 19:
            self.positions = self.place_piece(self.current_piece, self.positions)
            self.current_piece = Piece(-1, (3, -3))  
    count = 0  