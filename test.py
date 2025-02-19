import pygame
import numpy as np
import pickle
from FlappyBird import FlappyBirdEnv

with open("q_table.pkl", "rb") as f:
    q_table = pickle.load(f)

env = FlappyBirdEnv()
running = True
state = env.reset()
state = tuple(np.round(state, 5))
clock = pygame.time.Clock()

while running:
    env.render()

    if state in q_table:
        action = np.argmax(q_table[state])
    else:
        action = 0

    next_state, _, done = env.step(action)
    state = tuple(next_state)

    if done:
        print(f"Game Over! Score: {env.score}")
        running = False

    # clock.tick(30)
