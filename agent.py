import numpy as np
from constants.ActionSelectionType import Action
from constants.TDType import TD

class Agent:
    def __init__(self,
                 td_type,
                 action_selection,
                 alpha=0.1,
                 gamma=0.9,
                 epsilon=0.9,
                 epsilon_decay=0.999,
                 epsilon_min=0.01,
                 mu=0.2):
        self.action_size = 2
        self.td_type = td_type
        self.action_selection = action_selection
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.mu = mu
        self.q_table = {}

    def get_q_values(self, state):
        return self.q_table.setdefault(state, np.zeros(self.action_size))

    def choose_action(self, state):
        if self.action_selection == Action.EGREEDY:
            if np.random.uniform(0, 1) < self.epsilon:
                return np.random.choice(self.action_size)
            return np.argmax(self.get_q_values(state))
        else:
            return int(self.get_q_values(state)[1] > self.get_q_values(state)[0])


    def update_q_value(self, state, action, reward, next_state, next_action, done):
        q_values = self.get_q_values(state)
        q_next = self.get_q_values(next_state)

        if self.td_type == TD.QLEARNING:
            q_target = reward if done else reward + self.gamma * max(q_next)
            self.q_table[state][action] += self.alpha * (q_target - q_values[action])
        elif self.td_type == TD.SARSA:
            q_target = reward if done else reward + self.gamma * q_next[next_action]
            self.q_table[state][action] += self.alpha * (q_target - q_values[action])
        else:
            mu = 0.4
            self.q_table[state][action] = mu * self.q_table[state][action] + \
                                          (1 - mu) * (reward + max(self.q_table[next_state]))

    def decay_epsilon(self):
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
