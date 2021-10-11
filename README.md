# Sudoku Solver

This project was an excercise in the following programming subjects:
- Depth-first search and backtracking
- Object-oriented programming
- GUI design

### sudoku_solver.py
The original script generates a randomized sudoku and solves it using the backtracking algorithm.
Output is written to the terminal.

### sudoku_gui.py

The gui version allows the user to fill in the board by hand, not allowing incorrect placements.

#### Controls:
- Click any square to select it, selected squares are outlined in bright blue.
- With an empty square selected, press any of the number 1-9 keys to set it as a temporary value.
- If a selected square has a temporary value, pressing enter checks if the value was correct and places it on the board if so.
- If a selected square has a temporary value, pressing delete or backspace removes the temporary value.
- Pressing spacebar will solve the current board.
