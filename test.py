import numpy as np
import pickle
from FlappyBird import FlappyBirdEnv

with open("q_table_q_learning.pkl", "rb") as f:
    q_table = pickle.load(f)

env = FlappyBirdEnv(delay=10)
running = True
state = env.reset()

while running:
    env.render()

    if state in q_table:
        action = np.argmax(q_table[state])
    else:
        action = 0

    next_state, _, done = env.step(action)
    state = next_state

    if done:
        print(f"Game Over! Score: {env.score}")
        running = False

    # clock.tick(30)
