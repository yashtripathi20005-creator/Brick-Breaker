import pygame
from constants import *

class PowerUp:
    def __init__(self, x, y, powerup_type):
        self.rect = pygame.Rect(x - 10, y - 10, 20, 20)
        self.type = powerup_type
        self.speed_y = 3
        self.color = self.get_color()
        self.symbol = self.get_symbol()
    
    def get_color(self):
        if self.type == 'grow':
            return GREEN
        elif self.type == 'shrink':
            return RED
        elif self.type == 'multi':
            return YELLOW
        return WHITE
    
    def get_symbol(self):
        if self.type == 'grow':
            return '+'
        elif self.type == 'shrink':
            return '-'
        elif self.type == 'multi':
            return '×'
        return '?'
    
    def update(self):
        self.rect.y += self.speed_y
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        # Draw symbol
        font = pygame.font.Font(None, 20)
        text = font.render(self.symbol, True, BLACK)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)
        # Add border
        pygame.draw.rect(screen, WHITE, self.rect, 2)
