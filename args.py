import argparse
import os
from constants.ActionSelectionType import Action
from constants.TDType import TD


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        '--num_episodes',
        help='number of episodes, > 0',
        type=int,
        default=1000
    )
    parser.add_argument(
        '--td_type',
        help='Temporal difference types; possible are:'
             f'"{TD.SARSA}", "{TD.QLEARNING}", "{TD.EMAQLEARNING}"; default is "{TD.SARSA}"',
        type=str,
        default=TD.SARSA
    )
    parser.add_argument(
        '--action_selection',
        help='action selection type; possible are:'
             f'{Action.GREEDY}, "{Action.EGREEDY}"; default is "{Action.GREEDY}"',
        type=str,
        default=Action.GREEDY
    )
    parser.add_argument(
        '--alpha',
        help='alpha',
        type=float,
        default=0.1
    )
    parser.add_argument(
        '--gamma',
        help='gamma',
        type=float,
        default=0.9
    )
    parser.add_argument(
        '--epsilon',
        help='epsilon',
        type=float,
        default=0.9
    )
    parser.add_argument(
        "--epsilon_decay",
        help="epsilon_decay. default is None",
        type=float,
        default=None
    )
    parser.add_argument(
        '--epsilon_min',
        help='minimization of epsilon, used when epsilon_decay is not None.',
        type=float,
        default=0.1
    )
    parser.add_argument(
        "--mu",
        help='used when TD type is EMA Qlearning.'
             'default is `0.2`',
        type=float,
        default=0.2
    )
    parser.add_argument(
        "--log_dir",
        help='direction path of log file',
        type=str,
        default='experiment_1'
    )

    args = parser.parse_args()

    log_dir = os.path.join('logs', args.log_dir)

    if not os.path.isdir(log_dir):
        os.makedirs(log_dir)

    with open(os.path.join(log_dir, 'info.txt'), 'w') as f:
        for key, value in vars(args).items():
            f.write(f'{key}: {value}\n')

        f.close()

    args.log_dir = log_dir

    return args
