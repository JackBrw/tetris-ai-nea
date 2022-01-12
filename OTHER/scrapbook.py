loop = True
while loop:
    temp = False
    for block in default.get():
        x, y = block
        if x >0:
            temp = True
    if temp: default.left()
    loop = temp
default.right()