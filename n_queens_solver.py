class NQueensSolver:
    def __init__(self, N):
        self.N = N
        self.solutions = []
        self.metrics = []

    def is_safe(self, board, row, col):
        """Έλεγχος αν μια βασίλισσα μπορεί να τοποθετηθεί με ασφάλεια."""
        for i in range(row):
            if board[i] == col or \
               board[i] - i == col - row or \
               board[i] + i == col + row:
                return False
        return True
