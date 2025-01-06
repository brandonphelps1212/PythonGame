import os
import sys
import time
from grid import Grid

def clear_screen(grid_size):
    os.system('cls' if os.name == 'nt' else 'clear')
    title = "Brain Buster"
    total_width = grid_size * 6 + 3
    title_position = (total_width - len(title)) // 2
    print(" " * title_position + title + "\n")

def display_menu():
    print("\nMenu:")
    print("1. Let me select two elements")
    print("2. Uncover one element for me")
    print("3. I give up – reveal the grid")
    print("4. New game")
    print("5. Exit")
    print("Select: ", end='')

def convert_to_indices(cell):
    col = ord(cell[0].upper()) - ord('A')
    row = int(cell[1:])
    return row, col

def main():
    if len(sys.argv) != 2 or not sys.argv[1].isdigit() or int(sys.argv[1]) not in [2, 4, 6]:
        print("Usage: python3 game.py [2|4|6]")
        sys.exit(1)
    
    size = int(sys.argv[1])
    grid = Grid(size)
    clear_screen(size)
    grid.print_grid()

    while True:
        display_menu()
        choice = input()

        if choice == '1':
            first = input("Enter First Cell Coordinates (e.g., A0): ")
            second = input("Enter Second Cell Coordinates (e.g., A0): ")
            coords_first = convert_to_indices(first, size)
            coords_second = convert_to_indices(second, size)
            if not coords_first or not coords_second:
                clear_screen(size)
                grid.print_grid()
                print()
                print("Invalid coordinates. Please try again.")
                continue
            if coords_first == coords_second:
                clear_screen(size)
                grid.print_grid()
                print()
                print("Duplicate cells entered. Please enter different cells.")
                continue
            if isMatched(grid, first):
                clear_screen(size)
                grid.print_grid()
                print()
                print("Cell has already been matched")
                continue
            if isMatched(grid, second):
                clear_screen(size)
                grid.print_grid()
                print()
                print("Cell has already been matched")
                continue
            try:
                row1, col1 = convert_to_indices(first,size)
                row2, col2 = convert_to_indices(second,size)
                value1 = grid.reveal(row1, col1)
                value2 = grid.reveal(row2, col2)
                if value1 is not None and value2 is not None:
                    grid.guesses += 1
                    clear_screen(size)
                    grid.print_grid()
                    if value1 == value2:
                        grid.pairs_matched += 1  
                        print("It's a match!")
                        grid.matched_cells.add(first)
                        grid.matched_cells.add(second)

            
                    else:
                        print("No match. Hiding in 2 seconds...")
                        time.sleep(2)
                        grid.hide(row1, col1)
                        grid.hide(row2, col2)
            except (IndexError, ValueError):
                print("Invalid coordinates. Please try again.")
        elif choice == '2':
            cell = input("Enter the cell to uncover (e.g., A0): ")
            coords_cell= convert_to_indices(cell, size)
            if not coords_cell:
                clear_screen(size)
                grid.print_grid()
                print()
                print("Invalid coordinates. Please try again.")
                continue
            grid.guesses += 2
            try:
                row, col = convert_to_indices(cell, size)
                if not grid.visible[row][col]:
                    grid.reveal(row, col)
                clear_screen(size)
                grid.print_grid()
            except (IndexError, ValueError):
                print("Invalid coordinates. Please try again.")
        elif choice == '3':
            clear_screen(size)
            reveal_grid(grid)
            print()
            print("Don't give up so easily next time!")
            continue  
        elif choice == '4':
            grid.reset_grid()
        elif choice == '5':
            print("Thanks for playing!")
            break
        else:
            clear_screen(size)
            grid.print_grid()
            print()
            print("Invalid Choice, Please select options 1 - 5")
            continue

        if grid.is_complete():
            clear_screen(size)
            grid.print_grid()
            score = grid.score()
            if score > 0:
                print("\nYou've Won!")
                print(f"Your score: {score:.2f}")
            else:
                print("\nYou cheated Loser! Your score is 0!")
            continue
        clear_screen(size)
        grid.print_grid()
    
def convert_to_indices(cell, size):
    # Validate input format: must be one letter followed by numbers
    if len(cell) < 2 or not cell[0].isalpha() or not cell[1:].isdigit():
        return None
    col = ord(cell[0].upper()) - ord('A')
    row = int(cell[1:])
    # Validate that indices are within the bounds of the grid
    if 0 <= col < size and 0 <= row < size:
        return row, col
    return None

def reveal_grid(grid):
    for row in range(grid.size):
        for col in range(grid.size):
            grid.reveal(row, col)
    grid.print_grid()

def isMatched(grid, cell):
    return cell in grid.matched_cells



if __name__ == "__main__":
    main()