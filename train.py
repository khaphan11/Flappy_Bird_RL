from agent import Agent
from env import FlappyBirdEnv
import pickle
from args import parse_args
import pygame
import os


if __name__ == "__main__":
    args = parse_args()

    env = FlappyBirdEnv()
    agent = Agent(td_type=args.td_type,
                  action_selection=args.action_selection,
                  alpha=args.alpha,
                  gamma=args.gamma,
                  epsilon=args.epsilon,
                  epsilon_decay=args.epsilon_decay,
                  epsilon_min=args.epsilon_min,
                  mu=args.mu)

    num_episodes = args.num_episodes
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
            env.render(episode)

            if done or env.score > 3000:
                print(f"Episode {episode}, Score: {env.score}, Gift: {env.n_gift}, Epsilon: {agent.epsilon}, Total reward: {total_reward}")
                with open(os.path.join(args.log_dir, 'results.txt'), 'a') as f:
                    f.write(f"{episode}\t{env.score}\t{env.n_gift}\t{agent.epsilon}\t{total_reward}\n")
                f.close

                if args.epsilon_decay != None:
                    agent.decay_epsilon()

                break

        q_table = agent.q_table

        with open(os.path.join(args.log_dir, 'ckpt.pkl'), "wb") as f:
            pickle.dump(agent.q_table, f)

    pygame.quit()
