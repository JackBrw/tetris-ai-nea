num = 100
index = 0
for i in range(len(moves)):
    if holesList[i] < num:
        num = holesList[i]
        index = i