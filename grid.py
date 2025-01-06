import random

class Grid:
    def __init__(self, size):
        self.size = size
        self.grid = []
        self.visible = []
        self.guesses = 0  # Track the number of guesses made
        self.pair_attempts = 0  # Track the number of attempts to find pairs
        self.pairs_matched = 0
        self.matched_cells = set()
        self.initialize_grid()

    def initialize_grid(self):
        numbers = [i // 2 for i in range(self.size * self.size)]
        random.shuffle(numbers)
        self.grid = [numbers[i * self.size:(i + 1) * self.size] for i in range(self.size)]
        self.visible = [[False] * self.size for _ in range(self.size)]

    def reveal(self, row, col):
        if self.is_valid_position(row, col) and not self.visible[row][col]:
            self.visible[row][col] = True
            return self.grid[row][col]
        return None

    def hide(self, row, col):
        if self.is_valid_position(row, col):
            self.visible[row][col] = False

    def is_valid_position(self, row, col):
        return 0 <= row < self.size and 0 <= col < self.size

    def is_complete(self):
        # Check if all cells are revealed
        return all(all(cell for cell in row) for row in self.visible)

    def score(self):
        numberOfPairs =(self.size**2)//2
        if self.pairs_matched == numberOfPairs:
            score = (numberOfPairs / self.guesses) * 100
        elif self.guesses == (self.size**2) * 2:
            score = 0
        elif self.guesses > 0:
            score = (numberOfPairs / self.guesses) * 100
        return score

    def print_grid(self):
        print("   ", end='')
        for col in range(self.size):
            print(f"{chr(ord('A') + col):^5}", end='')
        print()

        for row in range(self.size):
            print(f"{row:>2} ", end='')
            for col in range(self.size):
                display_char = self.grid[row][col] if self.visible[row][col] else "X"
                print(f"{display_char:^5}", end='')
            print()

    def reset_grid(self):
        self.initialize_grid()
        self.guesses = 0
        self.pairs_matched = 0