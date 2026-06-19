import pygame
import math
from constants import *

class Ball:
    def __init__(self, x, y):
        self.radius = BALL_RADIUS
        self.color = BALL_COLOR
        self.x = x
        self.y = y
        self.speed_x = BALL_SPEED_X
        self.speed_y = BALL_SPEED_Y
        self.launched = False
        self.rect = pygame.Rect(x - self.radius, y - self.radius, 
                               self.radius * 2, self.radius * 2)
    
    def launch(self):
        self.launched = True
        # Randomize initial direction slightly
        angle = math.radians(45 + pygame.random.randint(-15, 15))
        speed = math.sqrt(self.speed_x**2 + self.speed_y**2)
        self.speed_x = speed * math.cos(angle)
        self.speed_y = -speed * math.sin(angle)
    
    def update(self):
        if self.launched:
            self.x += self.speed_x
            self.y += self.speed_y
            self.rect.x = self.x - self.radius
            self.rect.y = self.y - self.radius
    
    def bounce_x(self):
        self.speed_x = -self.speed_x
    
    def bounce_y(self):
        self.speed_y = -self.speed_y
    
    def reset(self, x, y):
        self.x = x
        self.y = y
        self.launched = False
        self.speed_x = BALL_SPEED_X
        self.speed_y = BALL_SPEED_Y
        self.rect.x = x - self.radius
        self.rect.y = y - self.radius
    
    def collides_with(self, rect):
        return self.rect.colliderect(rect)
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
