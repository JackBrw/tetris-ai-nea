import json, sys, os

def get():
    with open(os.path.join(sys.path[0], "weights.json"), "r") as file:
        data = json.load(file)
    return data

def save(data):
    with open(os.path.join(sys.path[0], "weights.json"), "w") as file:
        json.dump(data, file)
        
data = get()    