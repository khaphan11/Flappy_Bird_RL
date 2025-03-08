import numpy as np
import pickle
from env import FlappyBirdEnv
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--delay',
        type=int,
        default=10
    )
    parser.add_argument(
        '--ckpt',
        help='checkpoint path',
        type=str
    )
    args = parser.parse_args()

    with open(args.ckpt, "rb") as f:
        q_table = pickle.load(f)

    env = FlappyBirdEnv(delay=args.delay)
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
            print(f"Game Over! Score: {env.score}, Gift: {env.n_gift}")
            running = False
