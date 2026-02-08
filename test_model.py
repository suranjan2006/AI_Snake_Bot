from model.dqn import DQN
import torch

# 6 inputs (state size), 4 outputs (actions)
model = DQN(6, 4)

# Dummy state
state = torch.randn(6)

# Predict
output = model(state)

print("Q-values:", output)
