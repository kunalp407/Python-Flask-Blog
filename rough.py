import pygame
import random

# Constants
WIDTH = 400
HEIGHT = 600
FPS = 60
GROUND_HEIGHT = 50
PIPE_WIDTH = 50
GAP_HEIGHT = 200
GRAVITY = 0.25
FLAP_STRENGTH = 6

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# Load assets
bird_img = pygame.image.load('bird.png').convert_alpha()
pipe_img = pygame.image.load('pipe.png').convert_alpha()

# Functions
def draw_text(text, size, color, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

def draw_floor():
    screen.blit(floor_img, (floor_x, HEIGHT - GROUND_HEIGHT))

def draw_bird():
    screen.blit(bird_img, bird_rect)

def draw_pipe(pipe):
    screen.blit(pipe_img, pipe)

def flap():
    bird_rect.y -= FLAP_STRENGTH

def game_over():
    screen.fill(BLACK)
    draw_text("Game Over!", 64, WHITE, WIDTH/2, HEIGHT/4)
    draw_text("Press SPACE to Play Again", 22, WHITE, WIDTH/2, HEIGHT/2)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

# Game variables
bird_rect = bird_img.get_rect(center=(100, HEIGHT/2))
pipes = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1500)
score = 0

running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == SPAWNPIPE:
            pipe_height = random.randint(100, 400)
            top_pipe = pipe_img.get_rect(midbottom=(WIDTH, pipe_height - GAP_HEIGHT/2))
            bottom_pipe = pipe_img.get_rect(midtop=(WIDTH, pipe_height + GAP_HEIGHT/2))
            pipes.extend((top_pipe, bottom_pipe))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                flap()

    # Update
    bird_rect.y += GRAVITY
    for pipe in pipes:
        pipe.centerx -= 2
        if pipe.centerx <= -PIPE_WIDTH/2:
            pipes.remove(pipe)
        if pipe.colliderect(bird_rect):
            game_over()
    if bird_rect.top <= 0 or bird_rect.bottom >= HEIGHT - GROUND_HEIGHT:
        game_over()

    # Score
    for pipe in pipes:
        if pipe.centerx == bird_rect.centerx:
            score += 0.5
            print(score)

    # Draw
    screen.fill((0, 0, 0))
    draw_bird()
    for pipe in pipes:
        draw_pipe(pipe)
    draw_floor()
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
