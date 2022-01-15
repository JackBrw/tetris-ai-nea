
# holds the 7 grid positions for the pieces
def figures(figure): 
    figures = (
        (1, 5, 9, 13), #I piece [0]
        (1, 5, 8, 9), #J piece [1]
        (1, 5, 9, 10), #L piece [2]
        (5, 6, 9, 10), #O piece [3]
        (0, 4, 5, 9), #S piece [4]
        (0, 4, 5, 8), #T piece [5]
        (1, 4, 5, 8) #Z piece [6]
    )
    return(figures[figure])