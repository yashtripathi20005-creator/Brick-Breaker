import pygame
from constants import *
from paddle import Paddle
from ball import Ball
from brick import Brick
from powerup import PowerUp

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        self.reset_game()
    
    def reset_game(self):
        self.paddle = Paddle(
            SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2,
            SCREEN_HEIGHT - 40
        )
        self.ball = Ball(
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 60
        )
        self.bricks = self.create_bricks()
        self.powerups = []
        self.lives = LIVES
        self.score = 0
        self.game_over = False
        self.win = False
        self.ball_attached = True  # Ball starts attached to paddle
    
    def create_bricks(self):
        bricks = []
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                x = col * (BRICK_WIDTH + BRICK_PADDING) + BRICK_PADDING
                y = row * (BRICK_HEIGHT + BRICK_PADDING) + BRICK_TOP_OFFSET
                color = BRICK_COLORS[row % len(BRICK_COLORS)]
                bricks.append(Brick(x, y, BRICK_WIDTH, BRICK_HEIGHT, color, row))
        return bricks
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if self.ball_attached:
                    self.ball_attached = False
                    self.ball.launch()
                elif self.game_over or self.win:
                    self.reset_game()
            if event.key == pygame.K_r and (self.game_over or self.win):
                self.reset_game()
    
    def update(self):
        if self.game_over or self.win:
            return
        
        # Move paddle
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.paddle.move_left()
        if keys[pygame.K_RIGHT]:
            self.paddle.move_right()
        
        # Update ball
        if not self.ball_attached:
            self.ball.update()
            
            # Ball collision with walls
            if self.ball.x - BALL_RADIUS <= 0 or self.ball.x + BALL_RADIUS >= SCREEN_WIDTH:
                self.ball.bounce_x()
            
            if self.ball.y - BALL_RADIUS <= 0:
                self.ball.bounce_y()
            
            # Ball lost (below screen)
            if self.ball.y + BALL_RADIUS > SCREEN_HEIGHT:
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over = True
                else:
                    self.ball_attached = True
                    self.ball.reset(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60)
                    self.paddle.reset(SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, SCREEN_HEIGHT - 40)
                return
            
            # Ball collision with paddle
            if self.ball.collides_with(self.paddle.rect):
                self.ball.bounce_y()
                # Change angle based on where ball hits paddle
                hit_pos = (self.ball.x - self.paddle.rect.x) / PADDLE_WIDTH
                self.ball.speed_x = (hit_pos - 0.5) * 10
                if abs(self.ball.speed_x) < 1.5:
                    self.ball.speed_x = 1.5 if self.ball.speed_x >= 0 else -1.5
                self.ball.speed_y = -abs(self.ball.speed_y)
            
            # Ball collision with bricks
            for brick in self.bricks[:]:
                if brick.active and self.ball.collides_with(brick.rect):
                    # Determine bounce direction
                    overlap_left = self.ball.x + BALL_RADIUS - brick.rect.x
                    overlap_right = brick.rect.x + brick.rect.width - (self.ball.x - BALL_RADIUS)
                    overlap_top = self.ball.y + BALL_RADIUS - brick.rect.y
                    overlap_bottom = brick.rect.y + brick.rect.height - (self.ball.y - BALL_RADIUS)
                    
                    min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)
                    
                    if min_overlap == overlap_left or min_overlap == overlap_right:
                        self.ball.bounce_x()
                    else:
                        self.ball.bounce_y()
                    
                    brick.active = False
                    self.score += 10 * (BRICK_ROWS - brick.row)  # More points for higher bricks
                    
                    # Random powerup drop (20% chance)
                    if pygame.random.randint(1, 100) <= 20:
                        powerup_type = pygame.random.choice(['grow', 'shrink', 'multi'])
                        self.powerups.append(PowerUp(brick.rect.centerx, brick.rect.centery, powerup_type))
                    break
            
            # Check win condition
            if all(not brick.active for brick in self.bricks):
                self.win = True
        
        # Update powerups
        for powerup in self.powerups[:]:
            powerup.update()
            if powerup.rect.y > SCREEN_HEIGHT:
                self.powerups.remove(powerup)
            elif powerup.rect.colliderect(self.paddle.rect):
                self.apply_powerup(powerup.type)
                self.powerups.remove(powerup)
    
    def apply_powerup(self, powerup_type):
        if powerup_type == 'grow':
            self.paddle.width = min(PADDLE_WIDTH * 1.5, 200)
            self.paddle.rect.width = self.paddle.width
        elif powerup_type == 'shrink':
            self.paddle.width = max(PADDLE_WIDTH * 0.5, 50)
            self.paddle.rect.width = self.paddle.width
        elif powerup_type == 'multi':
            # Add extra balls - simple implementation: just increase score
            self.score += 50
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw bricks
        for brick in self.bricks:
            if brick.active:
                brick.draw(self.screen)
        
        # Draw paddle
        self.paddle.draw(self.screen)
        
        # Draw ball
        self.ball.draw(self.screen)
        
        # Draw powerups
        for powerup in self.powerups:
            powerup.draw(self.screen)
        
        # Draw UI
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        self.screen.blit(lives_text, (SCREEN_WIDTH - 120, 10))
        
        if self.ball_attached:
            info_text = self.small_font.render("Press SPACE to launch", True, WHITE)
            self.screen.blit(info_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50))
        
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            text1 = self.font.render("GAME OVER", True, RED)
            text2 = self.small_font.render("Press SPACE or R to restart", True, WHITE)
            self.screen.blit(text1, (SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 - 20))
            self.screen.blit(text2, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 20))
        
        if self.win:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            text1 = self.font.render("YOU WIN!", True, GREEN)
            text2 = self.small_font.render("Press SPACE or R to play again", True, WHITE)
            self.screen.blit(text1, (SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 - 20))
            self.screen.blit(text2, (SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 + 20))
