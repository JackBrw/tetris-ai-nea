import json, sys, os

#gets the weights from the weights.json file
def get():
    with open(os.path.join(sys.path[0], "weights.json"), "r") as file:
        data = json.load(file)
    return data

#saves the weights to the weights.json file
def save(data):
    with open(os.path.join(sys.path[0], "weights.json"), "w") as file:
        json.dump(data, file)
