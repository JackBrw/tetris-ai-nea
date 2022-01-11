from numpy.lib.function_base import copy
import pygame
import copy
import random
from piece import *
    
    
class Event: #Class that handles keys in for the AI
    type = None
    key = None

    def __init__(self, type, key):
        self.type = type
        self.key = key

class AI:
    def __init__(self) -> None:
        pass
            
            
    
