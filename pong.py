import pygame
from pygame import sprite, display, time, font, key, event
from pygame.locals import *
import time as pytime  # Import the standard time module and alias it to avoid confusion with pygame.time

# Initialize Pygame
pygame.init()

# Parent class for sprites
class GameSprite(sprite.Sprite):
    def __init__(self, color, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update_r(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - self.rect.height - 5:
            self.rect.y += self.speed
    
    def update_l(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - self.rect.height - 5:
            self.rect.y += self.speed

# Game scene:
back = (0, 0, 0)  # Background color
win_width = 600
win_height = 500
window = display.set_mode((win_width, win_height))
window.fill(back)

# Flags responsible for game state
game = True
finish = False
clock = time.Clock()
FPS = 60

# Creating ball and paddles   
racket1 = Player((255, 255, 255), 30, 200, 4, 30, 150) 
racket2 = Player((255, 255, 255), 520, 200, 4, 30, 150)
ball = GameSprite((255, 255, 255), 200, 200, 4, 50, 50)

# Initialize font
font.init()
game_font = font.Font(None, 35)  # Initialize game_font
lose1 = game_font.render('PLAYER 1 LOSE!', True, (180, 0, 0))
lose2 = game_font.render('PLAYER 2 LOSE!', True, (180, 0, 0))
win1 = game_font.render('PLAYER 1 WIN', True, (0, 255, 0))
win2 = game_font.render('PLAYER 2 WIN', True, (0, 255, 0))

# Initialize scores
score1 = 0
score2 = 0

# Ball speed
speed_x = 3
speed_y = 3

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    
    if not finish:
        window.fill(back)
        racket1.update_l()
        racket2.update_r()
        
        ball.rect.x += speed_x
        ball.rect.y += speed_y

        if sprite.collide_rect(racket1, ball) or sprite.collide_rect(racket2, ball):
            speed_x *= -1
        
        # If the ball reaches screen edges, change its movement direction
        if ball.rect.y > win_height - ball.rect.height or ball.rect.y < 0:
            speed_y *= -1

        # If ball flies behind this paddle, update score and reset ball position
        if ball.rect.x < 0:
            score2 += 1
            ball.rect.x, ball.rect.y = win_width // 2, win_height // 2
            speed_x *= -1  # Change ball direction
            speed_y *= -1
            window.blit(win2, (200, 200))
            display.update()
            pytime.sleep(3)
        
        if ball.rect.x > win_width - ball.rect.width:
            score1 += 1
            ball.rect.x, ball.rect.y = win_width // 2, win_height // 2
            speed_x *= -1  # Change ball direction
            speed_y *= -1
            window.blit(win1, (200, 200))
            display.update()
            pytime.sleep(2)

        # Check for winning condition
        if score1 >= 5:
            finish = True
            window.fill(back)  # Clear the screen
            window.blit(lose2, (200, 200))  # Player 1 wins
            display.update()  # Update the display to show the win message
            pytime.sleep(2)  # Pause for 2 seconds
            
        elif score2 >= 5:
            finish = True
            window.fill(back)  # Clear the screen
            window.blit(lose1, (200, 200))  # Player 2 wins
            display.update()  # Update the display to show the win message
            pytime.sleep(2)  # Pause for 2 seconds

        # Display scores
        score_text = game_font.render(f"Player 1: {score1}  Player 2: {score2}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(win_width // 2, 30))  # Center the score at the top
        window.blit(score_text, score_rect)

        racket1.reset()
        racket2.reset()
        ball.reset()

    display.update()
    clock.tick(FPS)

pygame.quit()
