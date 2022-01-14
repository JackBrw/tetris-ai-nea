for i in range(8):
    row = 450
    if i % 2 == 1: 
        row = 50
        column = (i-1)*100+50
    else:
        column = i*100+50
    print("----------------")
    print(f"{(50 + round(i/4)*300)} {row}")