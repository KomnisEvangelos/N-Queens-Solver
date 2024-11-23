from n_queens_solver import NQueensSolver
from methods.backtracking import BacktrackingSolver
from methods.bfs_dfs import BFSSolver, DFSSolver
from methods.a_star import AStarSolver
from methods.genetic import GeneticSolver
from methods.reinforcement import ReinforcementSolver
from methods.brute_force import BruteForceSolver
from visualizer import visualize_solution

N = 10

solver = NQueensSolver(N)
methods = [
    BacktrackingSolver,
    BFSSolver,
    DFSSolver,
    AStarSolver,
    GeneticSolver,
    #ReinforcementSolver,
    BruteForceSolver
]

for method in methods:
    print(f"Running {method.__name__}...")
    instance = method(N)
    instance.solve()
    solver.metrics.extend(instance.metrics)
    solver.solutions.extend(instance.solutions)

print("\nΑποτελέσματα Μετρικών:")
for metric in solver.metrics:
    print(metric)

if solver.solutions:
    visualize_solution(N, solver.solutions[0])
