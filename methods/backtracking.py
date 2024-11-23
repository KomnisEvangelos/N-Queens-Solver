import time
import os
from n_queens_solver import NQueensSolver
from visualizer import visualize_solution

class BacktrackingSolver(NQueensSolver):
    def __init__(self, N):
        super().__init__(N)
        self.all_solutions = []

    def solve(self):
        start_time = time.time()


        method_folder = f"backtracking_solutions_{self.N}"
        if not os.path.exists(method_folder):
            os.makedirs(method_folder)

        # Start backtracking from the first row
        self.backtrack([], 0)

        exec_time = time.time() - start_time
        self.metrics.append({
            "method": "Backtracking",
            "time": exec_time,
            "iterations": len(self.all_solutions),
            "efficiency": len(self.all_solutions) / exec_time if exec_time > 0 else 0,
            "solutions_found": len(self.all_solutions)
        })

    def backtrack(self, state, row):
        """Recursive backtracking method."""
        if row == self.N:
            solution_image_path = f"backtracking_solutions_{self.N}/solution_{len(self.all_solutions)}.png"
            visualize_solution(self.N, state, solution_image_path)
            #print(f"Solution found: {state}")
            self.all_solutions.append(state)
            return

        for col in range(self.N):
            if self.is_valid_move(state, row, col):
                self.backtrack(state + [col], row + 1)

    def is_valid_move(self, state, row, col):
        """Check if placing a queen at (row, col) is valid."""
        for i in range(row):
            if state[i] == col or abs(state[i] - col) == abs(i - row):
                return False
        return True
