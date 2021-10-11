
from random import sample, choice
import copy
def shuffle(s): return sample(s,len(s))

base  = 3
length = base*base
numbers = range(1,length+1)
# board = [[0 for x in range(length)]  for y in range(length)]

def fill_random(board, amount):
    for x in range(amount):
        board[choice(numbers)-1][choice(numbers)-1] = choice(numbers)

def correct(state):
    for i in range(length):
        row = no_duplicates(state[i])
        col = no_duplicates([state[r][i] for r in range(length)])
        quad = no_duplicates([state[r][c] for (r,c) in quad_indexes(i)])
        if not row or not col or not quad:
            return False
    return True

def check_move(state, row, col, n):
    # clone = copy.deepcopy(state)
    state[row][col] = n
    return correct(state)

def quad_indexes(i):
    quad_rows = list(range((i//base) * base, (i//base) * base + base))
    quad_cols = list(range((i%base * base) , (i%base * base + base)))
    quad_ids = [(r, c) for r in quad_rows for c in quad_cols]
    return quad_ids

def no_duplicates(item):
    only_entries = [i for i in item if i != 0]
    return len(only_entries) == len(set(only_entries))

# def next_empty_cell(board):
#     for row, r in board:
#         if 0 in row:
#             for col, c in row:
#                 if col == 0:
#                     return (r,c)

def solve(board, row, col):
    if (row == length - 1 and col == length):
        return True
    if (col == length):
        col = 0
        row += 1
    if (board[row][col] != 0):
        return solve(board, row, col+1)
    for n in numbers:
        if check_move(board, row, col, n):
            board[row][col] = n
            if solve(board, row, col+1):
                return True
        board[row][col] = 0
    return False

def generate_sudoku(n_filled):
    while(True):
        board = [[0 for x in range(length)]  for y in range(length)]
        fill_random(board, n_filled)
        if correct(board):
            clone = copy.deepcopy(board)
            if solve(clone, 0, 0):
                return board


if __name__ == "__main__" :
    board = generate_sudoku(30)
    for line in board: print(line)
    solve(board, 0, 0)
    for line in board: print(line)
