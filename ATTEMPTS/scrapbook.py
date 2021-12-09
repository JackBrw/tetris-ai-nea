colour = {
    "white":(255, 255, 255),
    "black":(0, 0, 0)
}

_locked_positions = {
    (4, 4):colour["white"],
    (3, 4):colour["black"]
}

def main(locked_positions):
    grid = [[(0, 0, 0) for x in range(5)] for y in range(5)]
    for x in range(5):
        for y in range(5):
            if (x, y) in locked_positions:
                grid[x][y] = locked_positions[(x, y)]
    print(grid[3][4])
    print(grid[4][4])
    
        

if __name__ == "__main__":
    main(_locked_positions)