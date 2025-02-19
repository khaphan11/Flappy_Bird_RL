import pygame
import random
import numpy as np
from sarsa import SARSAAgent
from FlappyBird import FlappyBirdEnv

pygame.init()

env = FlappyBirdEnv()
agent = SARSAAgent(state_size=4, action_size=2)

num_episodes = 1000
for episode in range(num_episodes):
    state = env.reset()
    state = tuple(np.round(state, 5))
    action = agent.choose_action(state)
    total_reward = 0

    while True:
        next_state, reward, done = env.step(action)
        next_state = tuple(np.round(next_state, 5))[0]
        # print(next_state)
        next_action = agent.choose_action(next_state)
        agent.update_q_value(state, action, reward, next_state, next_action, done)
        total_reward += reward
        state, action = next_state, next_action
        env.render()

        if done:
            # agent.decay_epsilon()
            print(f"Episode {episode}, Score: {env.score}, Epsilon: {agent.epsilon}, Total reward: {total_reward}")
            break

    # print(total_reward, env.score)


pygame.quit()

q_table = agent.q_table

import pickle
with open("q_table.pkl", "wb") as f:
    pickle.dump(agent.q_table, f)
