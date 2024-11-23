import matplotlib.pyplot as plt
import numpy as np


def visualize_solution(N, state, output_path):
    """Visualize and save the N-Queens solution."""
    board = [['.' for _ in range(N)] for _ in range(N)]
    for row, col in enumerate(state):
        board[row][col] = 'Q'

    fig, ax = plt.subplots()
    ax.matshow([[0 if cell == '.' else 1 for cell in row] for row in board], cmap="Blues")

    # Adding labels to the cells
    for (i, j), val in np.ndenumerate(board):
        ax.text(j, i, val, ha='center', va='center', color="red" if val == 'Q' else "black")

    plt.axis('off')  # Turn off the axis
    plt.savefig(output_path)
    plt.close()
