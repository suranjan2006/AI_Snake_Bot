import torch
import numpy as np
from test_env import SnakeGame
from model.dqn import LinearQNet


def get_state(game):

    head = game.snake[0]

    point_l = (head[0] - 20, head[1])
    point_r = (head[0] + 20, head[1])
    point_u = (head[0], head[1] - 20)
    point_d = (head[0], head[1] + 20)

    dir_l = game.direction == "LEFT"
    dir_r = game.direction == "RIGHT"
    dir_u = game.direction == "UP"
    dir_d = game.direction == "DOWN"

    state = [

        (dir_r and game.is_collision(point_r)) or
        (dir_l and game.is_collision(point_l)) or
        (dir_u and game.is_collision(point_u)) or
        (dir_d and game.is_collision(point_d)),

        (dir_u and game.is_collision(point_r)) or
        (dir_d and game.is_collision(point_l)) or
        (dir_l and game.is_collision(point_u)) or
        (dir_r and game.is_collision(point_d)),

        (dir_d and game.is_collision(point_r)) or
        (dir_u and game.is_collision(point_l)) or
        (dir_r and game.is_collision(point_u)) or
        (dir_l and game.is_collision(point_d)),

        dir_l,
        dir_r,
        dir_u,
        dir_d,

        game.food[0] < head[0],
        game.food[0] > head[0],
        game.food[1] < head[1],
        game.food[1] > head[1]
    ]

    return np.array(state, dtype=int)


def play():

    model = LinearQNet(11, 256, 3)
    model.load_state_dict(torch.load("snake_dqn.pth"))
    model.eval()

    game = SnakeGame()

    while True:

        state = get_state(game)
        state0 = torch.tensor(state, dtype=torch.float32)

        prediction = model(state0)
        move = torch.argmax(prediction).item()

        final_move = [0, 0, 0]
        final_move[move] = 1

        reward, done, score = game.play_step(final_move)

        if done:
            print("AI Score:", score)
            game.reset()


if __name__ == "__main__":
    play()
