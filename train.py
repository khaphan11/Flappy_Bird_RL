from sarsa import SARSAAgent
from FlappyBird import FlappyBirdEnv
import pickle

env = FlappyBirdEnv()
agent = SARSAAgent(state_size=4, action_size=2, alpha=0.1, gamma=0.9, epsilon=0.9)

num_episodes = 500
for episode in range(num_episodes):
    state = env.reset()
    action = agent.choose_action(state)
    total_reward = 0

    while True:
        next_state, reward, done = env.step(action)
        next_action = agent.choose_action(next_state)
        agent.update_q_value(state, action, reward, next_state, next_action, done)
        total_reward += reward
        state, action = next_state, next_action
        env.render()

        if done:
            # agent.decay_epsilon()
            print(f"Episode {episode}, Score: {env.score}, Epsilon: {agent.epsilon}, Total reward: {total_reward}")
            break

        if env.score > 3000:
            break

    q_table = agent.q_table

    with open("q_table_q_learning.pkl", "wb") as f:
        pickle.dump(agent.q_table, f)


# pygame.quit()
