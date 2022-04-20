def flip(value):
    return 'X' if value == 'O' else 'O'


class Board:
    def __init__(self, grid):
        self.grid = grid

    def get(self, x, y):
        if self.valid_point(x, y):
            return self.grid[y][x]
        return None

    def set(self, x, y, value):
        if self.valid_point(x, y):
            self.grid[y][x] = value
        else:
            raise ValueError('Position out of range')

    def flip(self, x, y):
        new_board = Board(self.grid)
        for curr_x in range(x-1, x+2):
            for curr_y in range(y-1, y+2):
                if curr_x == x and curr_y == y:
                    continue
                if new_board.valid_point(curr_x, curr_y):
                    new_board.set(
                        curr_x,
                        curr_y,
                        flip(self.get(curr_x, curr_y))
                    )
        return new_board

    def valid_point(self, x, y):
        if x < 0 or y < 0:
            return False
        if x >= len(self.grid[0]) and y >= len(self.grid):
            return False
        return True

    def is_complete(self, goal):
        flat = [value for sublist in self.grid for value in sublist]
        return sum(True for value in flat if value != goal) == 0

    def __str__(self):
        lines = []
        for row in range(0, len(self.grid)):
            lines.append(''.join(self.grid[row]))
        return '\n'.join(lines)



class State:
    def __init__(self, board):
        self.board = board

    def next(self):
        raise NotImplementedError()


with open('./input', 'r') as reader:
    grid = [list(line.strip()) for line in reader.readlines()]
    print(grid)
