import pygame


class Event():
    type = None
    key = None

    def __init__(self, type, key):
        self.type = type
        self.key = key


counter = 0
def run(grid, piece, width, height):
    global counter
    counter += 1
    if counter < 3:
        return []
    counter = 0
    e = Event(pygame.KEYDOWN, pygame.K_RIGHT)
    return [e]