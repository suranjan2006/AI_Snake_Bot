from env.snake_env import SnakeEnv
import random

env = SnakeEnv(render=True)

state = env.reset()

running = True

while not env.done:

    action = random.randint(0, 3)

    state, reward, done = env.step(action)

    if done:
        break

print("Game Over!")
