import pygame
from constants import *

class Brick:
    def __init__(self, x, y, width, height, color, row):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.row = row
        self.active = True
    
    def draw(self, screen):
        if self.active:
            pygame.draw.rect(screen, self.color, self.rect)
            # Add a subtle highlight
            pygame.draw.rect(screen, (min(255, self.color[0] + 50),
                                     min(255, self.color[1] + 50),
                                     min(255, self.color[2] + 50)),
                            self.rect, 2)
