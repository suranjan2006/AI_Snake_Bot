import pygame
import random
import numpy as np


class SnakeEnv:

    def __init__(self, render=False):

        pygame.init()

        self.WIDTH = 600
        self.HEIGHT = 600
        self.BLOCK = 20

        self.render = render

        if self.render:
            self.screen = pygame.display.set_mode(
                (self.WIDTH, self.HEIGHT)
            )
            pygame.display.set_caption("AI Snake")

        self.clock = pygame.time.Clock()

        self.reset()


    def reset(self):

        self.x = self.WIDTH // 2
        self.y = self.HEIGHT // 2

        self.dx = 0
        self.dy = 0

        self.snake = []
        self.length = 1

        self.food_x = random.randrange(
            0, self.WIDTH, self.BLOCK
        )
        self.food_y = random.randrange(
            0, self.HEIGHT, self.BLOCK
        )

        self.score = 0
        self.done = False

        return self.get_state()


    def get_state(self):

        return np.array([
            self.x,
            self.y,
            self.food_x,
            self.food_y,
            self.dx,
            self.dy
        ], dtype=np.float32)


    def step(self, action):

        # Actions: 0=Left,1=Right,2=Up,3=Down

        if action == 0:
            self.dx = -self.BLOCK
            self.dy = 0

        elif action == 1:
            self.dx = self.BLOCK
            self.dy = 0

        elif action == 2:
            self.dy = -self.BLOCK
            self.dx = 0

        elif action == 3:
            self.dy = self.BLOCK
            self.dx = 0


        self.x += self.dx
        self.y += self.dy

        head = [self.x, self.y]
        self.snake.append(head)

        if len(self.snake) > self.length:
            del self.snake[0]


        reward = 0


        # Eat food
        if self.x == self.food_x and self.y == self.food_y:

            self.food_x = random.randrange(
                0, self.WIDTH, self.BLOCK
            )
            self.food_y = random.randrange(
                0, self.HEIGHT, self.BLOCK
            )

            self.length += 1
            self.score += 10
            reward = 10


        # Wall collision
        if (
            self.x < 0 or self.x >= self.WIDTH or
            self.y < 0 or self.y >= self.HEIGHT
        ):
            self.done = True
            reward = -100


        # Self collision
        for part in self.snake[:-1]:
            if part == head:
                self.done = True
                reward = -100


        if self.render:
            self.draw()


        self.clock.tick(60)

        return self.get_state(), reward, self.done


    def draw(self):

        BLACK = (0, 0, 0)
        GREEN = (0, 200, 0)
        RED = (200, 0, 0)

        self.screen.fill(BLACK)

        # Food
        pygame.draw.rect(
            self.screen, RED,
            [self.food_x, self.food_y,
             self.BLOCK, self.BLOCK]
        )

        # Snake
        for part in self.snake:
            pygame.draw.rect(
                self.screen, GREEN,
                [part[0], part[1],
                 self.BLOCK, self.BLOCK]
            )

        pygame.display.update()
