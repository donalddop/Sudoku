# Sudoku Solver and GUI

This project explores the implementation of a Sudoku solver using a backtracking algorithm, coupled with an interactive graphical user interface (GUI). It served as an exercise in:
*   Depth-first search and backtracking algorithms
*   Object-oriented programming principles
*   GUI design and event handling

## Features

### Sudoku Solver (`sudoku_solver.py`)
*   Generates randomized Sudoku puzzles.
*   Solves Sudoku puzzles using a backtracking algorithm.
*   Outputs the generated and solved boards to the terminal.

### Sudoku GUI (`sudoku_gui.py`)
*   Provides an interactive graphical interface to play Sudoku.
*   Allows users to manually fill in the board, with basic validation.
*   Includes an animated solver that visually demonstrates the backtracking process.
*   Prevents incorrect placements based on Sudoku rules.

## Prerequisites

*   **Python 3.x**
*   **Pygame (for the GUI version)**

## Installation

1.  Clone the repository:
    ```bash
    git clone <repository_url>
    cd Sudoku
    ```
2.  Install the Pygame library (if you plan to use the GUI):
    ```bash
    pip install pygame
    ```

## Usage

### To run the command-line solver:
```bash
python sudoku_solver.py
```
This will generate a new Sudoku, print it to the terminal, solve it, and print the solved version.

### To run the GUI version:
```bash
python sudoku_gui.py
```
A Pygame window will open, displaying an interactive Sudoku board.

## Controls (GUI)

*   **Click any square:** Selects the square (outlined in bright blue).
*   **With an empty square selected, press 1-9:** Sets a temporary value in the selected square.
*   **With a temporary value selected, press Enter:** Checks if the temporary value is correct and places it permanently on the board if valid.
*   **With a temporary value selected, press Delete or Backspace:** Removes the temporary value.
*   **Press Spacebar:** Initiates the animated solver, which will attempt to solve the current board state visually.

## File Structure

*   `sudoku_solver.py`: Contains the core logic for Sudoku generation and solving using a backtracking algorithm. This is a command-line utility.
*   `sudoku_gui.py`: Implements the graphical user interface for the Sudoku game, utilizing Pygame, and integrates solving logic for interactive play.
