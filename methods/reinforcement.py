import random
import time
import os
import numpy as np
from n_queens_solver import NQueensSolver
from visualizer import visualize_solution  # Assuming you have a function for visualizing solutions

class ReinforcementSolver(NQueensSolver):
    def __init__(self, N, alpha=0.1, gamma=0.9, epsilon=0.1, episodes=1000):
        super().__init__(N)
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.episodes = episodes
        self.q_table = {}
        self.all_solutions = []

    def solve(self):
        start_time = time.time()


        method_folder = f"reinforcement_solutions_{self.N}"
        if not os.path.exists(method_folder):
            os.makedirs(method_folder)


        for state in self.get_all_possible_states():
            self.q_table[state] = [0] * self.N

        total_rewards = []
        for episode in range(self.episodes):
            state = self.random_initial_state()
            total_reward = 0

            while not self.is_goal_state(state):
                if random.random() < self.epsilon:
                    action = random.randint(0, self.N - 1)  # Explore
                else:
                    action = self.get_best_action(state)  # Exploit

                next_state = self.apply_action(state, action)
                reward = self.compute_reward(next_state)

                best_next_action = self.get_best_action(next_state)
                self.q_table[state][action] += self.alpha * (
                    reward + self.gamma * self.q_table[next_state][best_next_action] - self.q_table[state][action])

                state = next_state
                total_reward += reward

                if self.is_goal_state(state):

                    solution_image_path = f"{method_folder}/solution_{len(self.all_solutions)}.png"
                    visualize_solution(self.N, state, solution_image_path)
                    print(f"Solution found: {state}")
                    self.all_solutions.append(state)
                    break

            total_rewards.append(total_reward)

        exec_time = time.time() - start_time
        self.metrics.append({
            "method": "Reinforcement Learning",
            "time": exec_time,
            "iterations": self.episodes,
            "efficiency": len(self.all_solutions) / exec_time if exec_time > 0 else 0,
            "solutions_found": len(self.all_solutions)
        })

    def random_initial_state(self):
        """Generate a random initial state."""
        return tuple(random.sample(range(self.N), self.N))

    def get_all_possible_states(self):
        """Generate all possible states of the N-Queens problem."""
        return [tuple(p) for p in itertools.permutations(range(self.N))]

    def is_goal_state(self, state):
        """Check if the state is a valid solution."""
        return self.compute_reward(state) == 0

    def compute_reward(self, state):
        """Compute the reward for a given state (lower is better)."""
        conflicts = 0
        for i in range(self.N):
            for j in range(i + 1, self.N):
                if abs(state[i] - state[j]) == abs(i - j):
                    conflicts += 1
        return conflicts

    def apply_action(self, state, action):
        """Apply an action (place a queen in a given row)."""
        state = list(state)
        for row in range(self.N):
            if state[row] == -1:
                state[row] = action
                break
        return tuple(state)

    def get_best_action(self, state):
        """Get the best action based on the Q-table."""
        return np.argmax(self.q_table[state])
