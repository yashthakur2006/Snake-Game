import pygame
import random
import asyncio
import platform

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Snake and food
snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
snake_dir = (1, 0)
food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
score = 0

def setup():
    global snake, snake_dir, food, score
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    snake_dir = (1, 0)
    food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    score = 0

def update_loop():
    global snake, snake_dir, food, score
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_dir != (0, 1):
                snake_dir = (0, -1)
            elif event.key == pygame.K_DOWN and snake_dir != (0, -1):
                snake_dir = (0, 1)
            elif event.key == pygame.K_LEFT and snake_dir != (1, 0):
                snake_dir = (-1, 0)
            elif event.key == pygame.K_RIGHT and snake_dir != (-1, 0):
                snake_dir = (1, 0)

    # Move snake
    head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])
    snake.insert(0, head)

    # Check for food collision
    if head == food:
        score += 1
        food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    else:
        snake.pop()

    # Check for wall collision
    if head[0] < 0 or head[0] >= GRID_WIDTH or head[1] < 0 or head[1] >= GRID_HEIGHT or head in snake[1:]:
        setup()  # Reset game

    # Draw
    screen.fill(BLACK)
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    pygame.draw.rect(screen, RED, (food[0] * GRID_SIZE, food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    pygame.display.flip()

async def main():
    setup()
    while True:
        update_loop()
        await asyncio.sleep(1.0 / FPS)

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())
