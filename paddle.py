import pygame
from constants import *

class Paddle:
    def __init__(self, x, y):
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.color = PADDLE_COLOR
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, self.width, self.height)
    
    def move_left(self):
        self.x -= PADDLE_SPEED
        if self.x < 0:
            self.x = 0
        self.rect.x = self.x
    
    def move_right(self):
        self.x += PADDLE_SPEED
        if self.x + self.width > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.width
        self.rect.x = self.x
    
    def reset(self, x, y):
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.width = PADDLE_WIDTH
        self.rect.width = self.width
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
