import torch
import random
import numpy as np
from collections import deque

from test_env import SnakeGame
from model.dqn import LinearQNet, QTrainer


# =========================
# CONFIG
# =========================
MAX_MEMORY = 100_000
BATCH_SIZE = 256
LR = 0.001
EPISODES = 500


# =========================
# AGENT
# =========================
class Agent:

    def __init__(self):

        self.n_games = 0
        self.epsilon = 1.0
        self.gamma = 0.9
        self.best_score = 0

        self.memory = deque(maxlen=MAX_MEMORY)

        self.model = LinearQNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)


    # =========================
    # GET STATE
    # =========================
    def get_state(self, game):

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

            # Danger straight
            (dir_r and game.is_collision(point_r)) or
            (dir_l and game.is_collision(point_l)) or
            (dir_u and game.is_collision(point_u)) or
            (dir_d and game.is_collision(point_d)),

            # Danger right
            (dir_u and game.is_collision(point_r)) or
            (dir_d and game.is_collision(point_l)) or
            (dir_l and game.is_collision(point_u)) or
            (dir_r and game.is_collision(point_d)),

            # Danger left
            (dir_d and game.is_collision(point_r)) or
            (dir_u and game.is_collision(point_l)) or
            (dir_r and game.is_collision(point_u)) or
            (dir_l and game.is_collision(point_d)),

            # Direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,

            # Food location
            game.food[0] < head[0],
            game.food[0] > head[0],
            game.food[1] < head[1],
            game.food[1] > head[1]
        ]

        return np.array(state, dtype=int)


    # =========================
    # MEMORY
    # =========================
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))


    # =========================
    # TRAIN LONG MEMORY
    # =========================
    def train_long(self):

        if len(self.memory) < BATCH_SIZE:
            return

        mini_sample = random.sample(self.memory, BATCH_SIZE)
        states, actions, rewards, next_states, dones = zip(*mini_sample)

        states = torch.tensor(np.array(states), dtype=torch.float32)
        next_states = torch.tensor(np.array(next_states), dtype=torch.float32)
        actions = torch.tensor(actions, dtype=torch.long)
        rewards = torch.tensor(rewards, dtype=torch.float32)
        dones = torch.tensor(dones, dtype=torch.bool)

        self.trainer.train_step(
            states, actions, rewards, next_states, dones
        )


    # =========================
    # TRAIN SHORT MEMORY
    # =========================
    def train_short(self, state, action, reward, next_state, done):

        state = torch.tensor(state, dtype=torch.float32)
        next_state = torch.tensor(next_state, dtype=torch.float32)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float32)
        done = torch.tensor(done, dtype=torch.bool)

        self.trainer.train_step(
            state, action, reward, next_state, done
        )


    # =========================
    # ACTION
    # =========================
    def get_action(self, state):

        self.epsilon = max(0.01, 1 - self.n_games / 200)

        if random.random() < self.epsilon:
            return random.randint(0, 2)

        state0 = torch.tensor(state, dtype=torch.float32)
        prediction = self.model(state0)
        return torch.argmax(prediction).item()


# =========================
# TRAINING LOOP
# =========================
def train():

    agent = Agent()
    game = SnakeGame()

    while agent.n_games < EPISODES:

        state_old = agent.get_state(game)
        move = agent.get_action(state_old)

        final_move = [0, 0, 0]
        final_move[move] = 1

        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        agent.train_short(state_old, move, reward, state_new, done)
        agent.remember(state_old, move, reward, state_new, done)

        if done:

            game.reset()
            agent.n_games += 1
            agent.train_long()

            # Save best model only
            if score > agent.best_score:
                agent.best_score = score
                agent.model.save()
                print(f"New Best Model Saved ✅ | Score: {score}")

            print(
                f"Game {agent.n_games} | "
                f"Score: {score} | "
                f"Epsilon: {round(agent.epsilon,3)}",
                flush=True
            )

    print("Training Finished ✅")


# =========================
# RUN
# =========================
if __name__ == "__main__":
    train()
