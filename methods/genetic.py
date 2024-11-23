import random
import time
import os
from n_queens_solver import NQueensSolver
from visualizer import visualize_solution  # Assuming you have a function for visualizing solutions

class GeneticSolver(NQueensSolver):
    def __init__(self, N, population_size=100, generations=1000, mutation_rate=0.01):
        super().__init__(N)
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.all_solutions = set()

    def solve(self):
        start_time = time.time()


        method_folder = f"genetic_solutions_{self.N}"
        if not os.path.exists(method_folder):
            os.makedirs(method_folder)

        population = [self.random_state() for _ in range(self.population_size)]

        for generation in range(self.generations):
            # Evaluate population
            population = sorted(population, key=lambda state: self.compute_reward(state))
            new_population = population[:self.population_size // 2]

            # Crossover
            for i in range(self.population_size // 2):
                parent1, parent2 = random.sample(new_population, 2)
                child = self.crossover(parent1, parent2)
                new_population.append(child)

            # Mutation
            for i in range(self.population_size // 2, self.population_size):
                if random.random() < self.mutation_rate:
                    new_population[i] = self.mutate(new_population[i])

            # Add random diversity every 10 generations
            if generation % 10 == 0:
                new_population += [self.random_state() for _ in range(self.population_size // 5)]

            population = new_population


            for state in population:
                canonical_state = self.canonical_form(state)
                if self.is_goal_state(state) and canonical_state not in self.all_solutions:
                    self.all_solutions.add(canonical_state)
                    solution_image_path = f"{method_folder}/solution_{len(self.all_solutions) - 1}.png"
                    visualize_solution(self.N, state, solution_image_path)

            # Stop if all solutions are found
            if len(self.all_solutions) == self.expected_solutions_count():
                break

            # Adjust mutation rate if progress is slow
            if generation % 100 == 0 and len(self.all_solutions) < self.expected_solutions_count() // 2:
                self.mutation_rate = min(self.mutation_rate * 1.5, 0.1)

        exec_time = time.time() - start_time
        self.metrics.append({
            "method": "Genetic",
            "time": exec_time,
            "iterations": len(self.all_solutions),
            "efficiency": len(self.all_solutions) / exec_time if exec_time > 0 else 0,
            "solutions_found": len(self.all_solutions)
        })

    def random_state(self):
        """Generate a random state for the population."""
        return tuple(random.sample(range(self.N), self.N))

    def crossover(self, parent1, parent2):
        """Perform crossover between two parents."""
        crossover_point = random.randint(1, self.N - 1)
        child = parent1[:crossover_point] + parent2[crossover_point:]
        child = self.fix_state(child)


        if self.compute_similarity(child, parent1) > 0.8 or self.compute_similarity(child, parent2) > 0.8:
            child = self.random_state()
        return tuple(child)

    def mutate(self, state):
        """Mutate a given state by randomly swapping two queens."""
        state = list(state)
        i, j = random.sample(range(self.N), 2)
        state[i], state[j] = state[j], state[i]
        return tuple(state)

    def fix_state(self, state):
        """Ensure the state is a valid permutation (no duplicate columns)."""
        seen = set()
        fixed_state = []
        for col in state:
            while col in seen:
                col = random.choice(range(self.N))
            fixed_state.append(col)
            seen.add(col)
        return fixed_state

    def canonical_form(self, state):
        """Returns a canonical representation of the solution to handle symmetric solutions."""
        rotations = [state]
        for _ in range(3):
            state = tuple(state.index(i) for i in range(len(state)))
            rotations.append(state)
        reflections = [tuple(reversed(r)) for r in rotations]
        return min(rotations + reflections)

    def compute_similarity(self, state1, state2):
        """Compute similarity between two states."""
        return sum(1 for i in range(len(state1)) if state1[i] == state2[i]) / len(state1)

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

    def expected_solutions_count(self):
        """Calculate the number of unique solutions for N-Queens."""
        # Precomputed number of unique solutions for known N values
        precomputed_solutions = {1: 1, 4: 2, 8: 92, 10: 724, 12: 14200}
        return precomputed_solutions.get(self.N, 0)  # Default to 0 if not precomputed

