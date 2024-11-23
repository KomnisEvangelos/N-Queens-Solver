import time
import os
from collections import deque
from n_queens_solver import NQueensSolver
from visualizer import visualize_solution


class BFSSolver(NQueensSolver):
    def __init__(self, N):
        super().__init__(N)
        self.all_solutions = []

    def solve(self):
        start_time = time.time()


        method_folder = f"bfs_solutions_{self.N}"
        if not os.path.exists(method_folder):
            os.makedirs(method_folder)

        # BFS setup: queue starts with an empty board (-1 indicates no queen in a row)
        queue = deque([[-1] * self.N])  # Initial empty state (list of -1)
        solutions_found = 0

        while queue:
            state = queue.popleft()


            if self.is_goal_state(state):
                self.all_solutions.append(state)
                solution_image_path = f"{method_folder}/solution_{solutions_found}.png"
                visualize_solution(self.N, state, solution_image_path)  # Save solution image
                solutions_found += 1
                continue


            for next_state in self.get_possible_next_states(state):
                queue.append(next_state)

        exec_time = time.time() - start_time
        self.metrics.append({
            "method": "BFS",
            "time": exec_time,
            "solutions_found": solutions_found,
            "efficiency": solutions_found / exec_time if exec_time > 0 else 0,
        })

    def is_goal_state(self, state):
        """Check if the state is a valid solution."""
        return -1 not in state and self.is_valid_board(state)

    def get_possible_next_states(self, state):
        """Generate all valid next states by placing a queen in the next row."""
        next_row = state.index(-1)
        next_states = []

        for col in range(self.N):
            if self.is_valid_move(state, next_row, col):
                new_state = state.copy()
                new_state[next_row] = col
                next_states.append(new_state)

        return next_states

    def is_valid_move(self, state, row, col):
        """Check if placing a queen at (row, col) is valid."""
        for r in range(row):
            if state[r] == col or abs(state[r] - col) == abs(r - row):
                return False
        return True

    def is_valid_board(self, state):
        """Check if the entire board configuration is valid (no conflicts)."""
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                    return False
        return True


class DFSSolver(NQueensSolver):
    def __init__(self, N):
        super().__init__(N)
        self.all_solutions = []

    def solve(self):
        start_time = time.time()


        method_folder = f"dfs_solutions_{self.N}"
        if not os.path.exists(method_folder):
            os.makedirs(method_folder)

        # DFS setup: stack starts with an empty board
        stack = [[-1] * self.N]  # Initial empty state (list of -1)
        solutions_found = 0

        while stack:
            state = stack.pop()


            if self.is_goal_state(state):
                self.all_solutions.append(state)
                solution_image_path = f"{method_folder}/solution_{solutions_found}.png"
                visualize_solution(self.N, state, solution_image_path)  # Save solution image
                solutions_found += 1
                continue


            for next_state in self.get_possible_next_states(state):
                stack.append(next_state)

        exec_time = time.time() - start_time
        self.metrics.append({
            "method": "DFS",
            "time": exec_time,
            "solutions_found": solutions_found,
            "efficiency": solutions_found / exec_time if exec_time > 0 else 0,
        })

    def is_goal_state(self, state):
        """Check if the state is a valid solution."""
        return -1 not in state and self.is_valid_board(state)

    def get_possible_next_states(self, state):
        """Generate all valid next states by placing a queen in the next row."""
        next_row = state.index(-1)
        next_states = []

        for col in range(self.N):
            if self.is_valid_move(state, next_row, col):
                new_state = state.copy()
                new_state[next_row] = col
                next_states.append(new_state)

        return next_states

    def is_valid_move(self, state, row, col):
        """Check if placing a queen at (row, col) is valid."""
        for r in range(row):
            if state[r] == col or abs(state[r] - col) == abs(r - row):  # Same column or diagonal
                return False
        return True

    def is_valid_board(self, state):
        """Check if the entire board configuration is valid (no conflicts)."""
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                    return False
        return True
