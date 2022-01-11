import pygame
from piece import *
    
    
class Event: #Class that handles keys in for the AI
    type = None
    key = None

    def __init__(self, type, key):
        self.type = type
        self.key = key

class AI:
    def __init__(self) -> None:
        self.counter = 0
        
    
    def proc(self):
        self.counter += 1
        if self.counter < 20:
            return []
        self.counter = 0
        e = Event(pygame.KEYDOWN, pygame.K_UP)
        return [e] #*MUST RETURN THE KEY AS A LIST