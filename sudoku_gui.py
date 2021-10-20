import pygame
from random import sample, choice

class Board:
    """ The Sudoku board class contains methods for generating and
    solving sudoku games. The class uses an array of Square objects to
    keep track of the game."""
    def __init__(self, rows, cols, height, width, win):
        self.rows = rows
        self.cols = cols
        self.height = height
        self.width = width
        self.win = win
        self.squares = [[Square(0, row, col, height, width) for row in range(rows)] for col in range(cols)]
        self.generate_sudoku(78)
        self.selected = None
        self.state = []
        self.update_state()

    def generate_sudoku(self, n_empty):
        """ Generate a Sudoku with n_empty empty squares. """
        empty_squares = 0
        selection = choice(range(self.rows))
        values = sample(range(1,10),9)
        for sq in self.squares[selection]:
            sq.set(values.pop())
        self.update_state()
        if self.solve_state():
            for row in range(self.rows):
                for col in range(self.cols):
                    self.squares[row][col].set(self.state[row][col])
            while n_empty != empty_squares:
                row = choice(range(9))
                col = choice(range(9))
                if self.squares[row][col].value != 0:
                    self.squares[row][col].set(0)
                    empty_squares += 1
        self.update_state()

    def update_state(self):
        """ Update the current state based on the squares array. """
        rows = range(self.rows)
        cols = range(self.cols)
        self.state = [[self.squares[row][col].value for col in cols] for row in rows]

    def sketch(self, row, col, value):
        """ Fill in temporary value. """
        self.squares[row][col].set_temp(value)

    def clear(self, row, col):
        """ Clear temporary value. """
        self.squares[row][col].set_temp(0)

    def draw_board(self):
        """ Draw the board and fill in values from squares array. """
        dif = self.width / self.cols
        for i in range(self.rows + 1):
            if i % 3 == 0 :
                thick = 7
            else:
                thick = 1
            pygame.draw.line(self.win, (0, 0, 0), (0, i * dif), (500, i * dif), thick)
            pygame.draw.line(self.win, (0, 0, 0), (i * dif, 0), (i * dif, 500), thick)
        for i in range(self.rows):
            for j in range(self.cols):
                self.squares[i][j].draw(self.win)

    def valid_move(self, row, col, val):
        """ Check if the move does not break any of the rules. """
        if val not in self.state[row]:
            if val not in [self.state[r][col] for r in range(9)]:
                if val not in [self.state[r][c] for (r,c) in self.quad_ids(row, col)]:
                    return True
        return False

    def check_move(self, val):
        """ Check if the move results in a solvable board. """
        row, col = self.selected
        if self.state[row][col] == 0:
            if self.valid_move(row, col, val):
                self.squares[row][col].set(val)
                self.update_state()
                if self.solve_state():
                    return True
                else:
                    self.squares[row][col].set(0)
                    self.squares[row][col].set_temp(0)
                    self.update_state()
        return False

    def solve_state(self):
        """ Try to solve the current board state. """
        empty_square = self.find_empty()
        if empty_square == None:
            return True
        else:
            row, col = empty_square

        for i in range(1,10):
            if self.valid_move(row, col, i):
                self.state[row][col] = i

                if self.solve_state():
                    return True
                self.state[row][col] = 0
        return False

    def solve_animated(self, win):
        """ Solve the board while drawing every solving step. """
        empty_square = self.find_empty()
        if empty_square == None:
            return True
        else:
            row, col = empty_square

        for i in range(1,10):
            if self.valid_move(row, col, i):
                self.squares[row][col].set(i)
                self.update_state()
                self.squares[row][col].draw_update(win, True)
                pygame.display.update()
                pygame.time.delay(100)
                if self.solve_animated(win):
                    return True
                self.squares[row][col].set(0)
                self.update_state()
                self.squares[row][col].draw_update(win, False)
                pygame.display.update()
                pygame.time.delay(100)
        return False

    def quad_ids(self, row, col):
        """ Return indexes for all squares in the same quadrant. """
        x = col // 3
        y = row // 3
        ids = []
        for i in range(y*3, y*3 + 3):
            for j in range(x * 3, x*3 + 3):
                ids.append((i,j))
        return ids

    def find_empty(self):
        """ Find the next empty square on the board. """
        for i in range(9):
            for j in range(9):
                if self.state[i][j] == 0:
                    return (i, j)  # row, col
        return None

    def get_square(self, pos):
        """ Get the square indexes for the current cursor position. """
        if 0 <= pos[0] <= self.width and 0 <= pos[1] <= self.height:
            dif = self.width / self.cols
            col = pos[0] // dif
            row = pos[1] // dif
            return (int(row), int(col))
        return None

class Square:
    """ The Square class holds a value, row and column. It's drawing
    functions use the given window measurements to correctly place each
    square. """
    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        """ Draw the square and its contents. """
        dif = self.width / 9
        x = self.row * dif
        y = self.col * dif
        if self.value != 0:
            fnt = pygame.font.SysFont("comicsans", 40)
            im = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(im, (x + dif/3, y))
        if self.temp != 0:
            fnt = pygame.font.SysFont("comicsans", 20)
            im = fnt.render(str(self.temp), 1, (0, 0, 0))
            win.blit(im, (x + dif/3, y))
        if self.selected:
            pygame.draw.rect(win, (0, 255, 255), (x, y, dif, dif), 4)

    def draw_update(self, win, current_path = True):
        """ Draw the square and its contents, keeping track of the path. """
        fnt = pygame.font.SysFont("comicsans", 40)
        dif = self.width / 9
        x = self.row * dif
        y = self.col * dif
        if self.value != 0:
            pygame.draw.rect(win, (255, 255, 255), (x, y, dif, dif), 0)
            im = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(im, (x + dif/3, y))
        if current_path:
            pygame.draw.rect(win, (0, 255, 0), (x, y, dif, dif), 3)
        else:
            pygame.draw.rect(win, (255, 0, 0), (x, y, dif, dif), 3)

    def set(self, val):
        self.value = val
    def set_temp(self, val):
        self.temp = val

class App:
    """ The App class contains the PyGame instance. """
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.height, self.width = 500, 500
        self.dif = self.height / 9
        pygame.font.init()
        self.font1 = pygame.font.SysFont("comicsans", 40)
        self.sudoku = None

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size)
        self.sudoku = Board(9,9,500,500,self._display_surf)
        self._running = True

    def on_event(self, event):
        """ When closing window. """
        if event.type == pygame.QUIT:
            self._running = False

        """ When clicking. """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                square = self.sudoku.get_square(event.pos)
                if square:
                    for row in range(self.sudoku.rows):
                        for col in range(self.sudoku.cols):
                            self.sudoku.squares[row][col].selected = False
                    self.sudoku.squares[square[0]][square[1]].selected = True
                    self.sudoku.selected = square

        """ When keyboard button is pressed. """
        if event.type == pygame.KEYDOWN:
            if self.sudoku.selected != None:
                row, col = self.sudoku.selected
                # Number 1 through 9
                if event.key in range(pygame.K_1, pygame.K_9 + 1):
                    value = event.key - 48
                    self.sudoku.sketch(row, col, value)

                # Delete or Backspace
                if event.key in [8, 127]:
                    self.sudoku.clear(row, col)

                # Spacebar
                if event.key == 32:
                    if self.sudoku.solve_animated(self._display_surf):
                        print('solved!')

                # Enter
                if event.key == 13:
                    temp = self.sudoku.squares[row][col].temp
                    if temp != 0:
                        if self.sudoku.valid_move(row, col, temp):
                            if self.sudoku.check_move(temp):
                                print("Correct move.")
                                self.sudoku.squares[row][col].set(temp)
                            else:
                                print("Incorrect move.")
                        else:
                            print("Illegal move.")
                        self.sudoku.squares[row][col].temp = 0
                        self.sudoku.update_state()

    def on_loop(self):
        pass

    def on_render(self):
        """ Drawing routine. """
        self._display_surf.fill((255, 255, 255))
        self.sudoku.draw_board()
        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        """ The main loop. """
        if self.on_init() == False:
            self._running = False
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
