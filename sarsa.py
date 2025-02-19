import numpy as np

class SARSAAgent:
    def __init__(self, state_size, action_size, alpha=0.1, gamma=0.9, epsilon=0.9, epsilon_decay=0.999, epsilon_min=0.01):
        self.state_size = state_size
        self.action_size = action_size
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.q_table = {}

    def get_q_values(self, state):
        return self.q_table.setdefault(state, np.zeros(self.action_size))

    def choose_action(self, state):
        if np.random.uniform(0, 1) < self.epsilon:
            return np.random.choice(self.action_size)
        return np.argmax(self.get_q_values(state))


    def update_q_value(self, state, action, reward, next_state, next_action, done):
        q_values = self.get_q_values(state)
        q_next = self.get_q_values(next_state)

        q_target = reward if done else reward + self.gamma * max(q_next)
        self.q_table[state][action] += self.alpha * (q_target - q_values[action])

        # self.q_table[state][action] = 0.1 * self.q_table[state][action] + \
        #                               (0.9) * (reward + max(q_next))

    def decay_epsilon(self):
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
