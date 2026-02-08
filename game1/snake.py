import pygame
import random

# Initialize pygame
pygame.init()

# Screen size
WIDTH = 600
HEIGHT = 600
BLOCK = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 25)


# Draw score
def show_score(score):
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))


# Main game function
def game_loop():

    # Snake starting position
    x = WIDTH // 2
    y = HEIGHT // 2

    dx = 0
    dy = 0

    snake = []
    length = 1

    # Food position
    food_x = random.randrange(0, WIDTH, BLOCK)
    food_y = random.randrange(0, HEIGHT, BLOCK)

    score = 0
    running = True

    while running:

        screen.fill(BLACK)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:
                    dx = -BLOCK
                    dy = 0

                elif event.key == pygame.K_RIGHT:
                    dx = BLOCK
                    dy = 0

                elif event.key == pygame.K_UP:
                    dy = -BLOCK
                    dx = 0

                elif event.key == pygame.K_DOWN:
                    dy = BLOCK
                    dx = 0

        # Move snake
        x += dx
        y += dy

        head = [x, y]
        snake.append(head)

        if len(snake) > length:
            del snake[0]

        # Eat food
        if x == food_x and y == food_y:
            food_x = random.randrange(0, WIDTH, BLOCK)
            food_y = random.randrange(0, HEIGHT, BLOCK)

            length += 1
            score += 10

        # Wall collision
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            running = False

        # Self collision
        for part in snake[:-1]:
            if part == head:
                running = False

        # Draw food
        pygame.draw.rect(
            screen, RED, [food_x, food_y, BLOCK, BLOCK]
        )

        # Draw snake
        for part in snake:
            pygame.draw.rect(
                screen, GREEN, [part[0], part[1], BLOCK, BLOCK]
            )

        show_score(score)

        pygame.display.update()
        clock.tick(12)

    pygame.quit()


# Run game
game_loop()
