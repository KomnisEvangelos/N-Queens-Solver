import time
import os
from itertools import permutations
from n_queens_solver import NQueensSolver
from visualizer import visualize_solution


class BruteForceSolver(NQueensSolver):
    def __init__(self, N):
        super().__init__(N)
        self.all_solutions = []

    def solve(self):
        start_time = time.time()

        method_folder = f"brute_force_solutions_{self.N}"
        if not os.path.exists(method_folder):
            os.makedirs(method_folder)

        for perm in permutations(range(self.N)):
            if self.is_goal_state(perm):
                # Save solution image
                solution_image_path = f"{method_folder}/solution_{len(self.all_solutions)}.png"
                visualize_solution(self.N, perm, solution_image_path)

                self.all_solutions.append(perm)

        exec_time = time.time() - start_time
        self.metrics.append({
            "method": "Brute Force",
            "time": exec_time,
            "iterations": len(self.all_solutions),
            "efficiency": len(self.all_solutions) / exec_time if exec_time > 0 else 0,
            "solutions_found": len(self.all_solutions)
        })

    def is_goal_state(self, state):
        """Check if the state is a valid solution (no attacking queens)."""
        return self.compute_reward(state) == 0

    def compute_reward(self, state):
        """Compute the reward for a given state (lower is better)."""
        conflicts = 0
        for i in range(self.N):
            for j in range(i + 1, self.N):
                if abs(state[i] - state[j]) == abs(i - j):  # Diagonal conflict
                    conflicts += 1
        return conflicts
