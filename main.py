from queue import SimpleQueue

def flip(value):
    return 'X' if value == 'O' else 'O'


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Board:
    def __init__(self, grid):
        self.grid = []
        for r in range(0, len(grid)):
            next_row = []
            for c in range(0, len(grid[r])):
                next_row.append(grid[r][c])
            self.grid.append(next_row)
        self.width = len(grid[0])
        self.height = len(grid)

    def get(self, x, y):
        if self.valid_point(x, y):
            return self.grid[y][x]
        return None

    def set(self, x, y, value):
        if self.valid_point(x, y):
            self.grid[y][x] = value
        else:
            raise ValueError('Position out of range')

    def neighbors(self, x, y):
        result = []
        for curr_x in range(x-1, x+2):
            for curr_y in range(y-1, y+2):
                if curr_x == x and curr_y == y:
                    continue
                if self.valid_point(curr_x, curr_y):
                    result.append(Point(curr_x, curr_y))
        return result

    def flip(self, x, y):
        new_board = Board(self.grid)
        for point in self.neighbors(x, y):
            new_board.set(point.x, point.y, flip(self.get(point.x, point.y)))
        return new_board

    def valid_point(self, x, y):
        return x >= 0 and x < self.width and y >= 0 and y < self.height

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
        next_states = []
        for x in range(0, self.board.width):
            for y in range(0, self.board.height):
                next_states.append(State(self.board.flip(x, y)))
        return next_states


class StateTreeNode:
    def __init__(self, state):
        self.state = state
        self.parent = None
        self.children = []

    def add_child(self, node):
        self.children.append(node)
        node.parent = self
        
    def path(self):
        backtrack = []
        curr_node = self
        while curr_node != None:
            backtrack.append(curr_node.state)
            curr_node = curr_node.parent
        return list(reversed(backtrack))


with open('./input', 'r') as reader:
    grid = [list(line.strip()) for line in reader.readlines()]

    root = StateTreeNode(State(Board(grid)))
    queue = SimpleQueue()
    queue.put(root)
    visited = set()
    visited.add(str(root.state.board))
    found = None
    state_count = 0
    while not queue.empty():
        node = queue.get()
        if node.state.board.is_complete('X'):
                found = node
                break

        for state in node.state.next():
            if str(state.board) not in visited:
                state_count += 1
                if state_count % 1000 == 0:
                    print('Searcing ' + str(state_count) + '...')
                child = StateTreeNode(state)
                node.add_child(child)
                queue.put(child)
                visited.add(str(state.board))

    if found:
        path = found.path()
        for i in range(0, len(path)):
            print('-- Step {step} --\n{grid}'.format(
                step=str(i+1),
                grid=str(path[i].board)
            ))
    else:
        print('No solution found')

