import time
import os
import heapq
from n_queens_solver import NQueensSolver
from visualizer import visualize_solution

class AStarSolver(NQueensSolver):
    def __init__(self, N):
        super().__init__(N)
        self.all_solutions = []

    def solve(self):
        start_time = time.time()


        method_folder = f"a_star_solutions_{self.N}"
        if not os.path.exists(method_folder):
            os.makedirs(method_folder)


        open_list = []
        heapq.heappush(open_list, (0, [-1] * self.N))
        g_cost = {tuple([-1] * self.N): 0}
        solutions_found = 0

        while open_list:
            _, state = heapq.heappop(open_list)
            state_tuple = tuple(state)

            if self.is_goal_state(state):
                self.all_solutions.append(state_tuple)
                solution_image_path = f"{method_folder}/solution_{solutions_found}.png"
                visualize_solution(self.N, state, solution_image_path)
                solutions_found += 1
                continue


            for next_state in self.get_possible_next_states(state):
                next_state_tuple = tuple(next_state)
                g_cost_new = g_cost[state_tuple] + 1
                f_cost = g_cost_new + self.heuristic(next_state)

                if next_state_tuple not in g_cost or g_cost_new < g_cost[next_state_tuple]:
                    g_cost[next_state_tuple] = g_cost_new
                    heapq.heappush(open_list, (f_cost, next_state))

        exec_time = time.time() - start_time
        self.metrics.append({
            "method": "A*",
            "time": exec_time,
            "solutions_found": solutions_found,
            "efficiency": solutions_found / exec_time if exec_time > 0 else 0,
        })

    def is_goal_state(self, state):
        """Check if the state is a valid solution (no attacking queens)."""
        return -1 not in state and self.is_valid_board(state)

    def get_possible_next_states(self, state):
        """Generate all valid next states by placing queens in the next row."""
        next_states = []
        next_row = state.index(-1)

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

    def compute_reward(self, state):
        """Compute the reward for a given state (lower is better)."""
        conflicts = 0
        for i in range(self.N):
            for j in range(i + 1, self.N):
                if abs(state[i] - state[j]) == abs(i - j):  # Diagonal conflict
                    conflicts += 1
        return conflicts

    def heuristic(self, state):
        """Heuristic function to estimate cost to reach the goal (number of conflicts)."""
        return self.compute_reward(state)
