from random import choice

class ARCPuzzle:
    """
    A class to represent the state and the possible transformation
    actions of an ARC puzzle or partially transformed ARC puzzle
    """

    def __init__(self, state):
        self.state = tuple((tuple(row) for row in state))

    def __hash__(self):
        return hash(self.state)

    def __eq__(self, other):
        if isinstance(other, ARCPuzzle):
            return self.state == other.state
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return str(self)

    def __str__(self):
        out = ""
        for row in self.state:
            out += str(row) + "\n"
        return out

    def copy(self):
        """
        Makes a deep copy of an ARCPuzzle object.
        """
        new = ARCPuzzle(self.state)
        return new

    def randomize(self, num_shuffles):
        """
        Randomizes an ARCPuzzle by executing a random action `num_suffles`
        times.
        """
        for i in range(num_shuffles):
            actions = [a for a in self.legalActions()]
            a = choice(actions)
            # print(actions, a)
            self.executeAction(a)

        return self

    def tophalf(self, grid):
        """ upper half """
        return grid[:len(grid) // 2]


    def rot90(self, grid):
        """ clockwise rotation by 90 degrees """
        return tuple(zip(*grid[::-1]))


    def hmirror(self, grid):
        """ mirroring along horizontal """
        return grid[::-1]

    def vmirror(self, grid):
        """ mirroring along horizontal """
        return tuple(reversed(grid))

    def lshift(self, grid):
        return tuple([tuple([e for e in row if e != 0] + [0]*row.count(0))
                      for row in grid])

    def compress(self, grid):
        """ removes frontiers """
        ri = [i for i, r in enumerate(grid) if len(set(r)) == 1]
        ci = [j for j, c in enumerate(zip(*grid)) if len(set(c)) == 1]
        return tuple([tuple([v for j, v in enumerate(r) if j not in ci])
                      for i, r in enumerate(grid) if i not in ri])

    def mapcolor(self, grid, a, b):
        return tuple(tuple(b if e == a else e for e in row) for row in grid)

    def trim(self, grid):
        """ removes border """
        return tuple(r[1:-1] for r in grid[1:-1])

    def executeAction(self, action):
        """
        Executes an action to the ARCPuzzle object.

        :param action: the action to execute
        :type action: "up", "left", "right", or "down"
        """
        if action == 'tophalf':
            self.state = self.tophalf(self.state)
        elif action == 'rot90':
            self.state = self.rot90(self.state)
        elif action == 'hmirror':
            self.state = self.hmirror(self.state)
        elif action == 'vmirror':
            self.state = self.vmirror(self.state)
        elif action == 'lshift':
            self.state = self.lshift(self.state)
        elif action == 'compress':
            self.state = self.compress(self.state)
        elif action[:8] == 'mapcolor':
            args = action[9:-1].split(',')
            self.state = self.mapcolor(self.state, int(args[0]), int(args[1]))
        else:
            raise RuntimeError("Not an action")

    ## color space is the set of colors present in either the input or the output image
    def legalActions(self, color_space=set(range(10))):
        """
        Returns an iterator to the legal actions that can be executed in the
        current state.
        """
        for action in ['tophalf', 'rot90', 'hmirror', 'vmirror', 'lshift', 'compress']:
            yield action

        for a in set(e for row in self.state for e in row):
            for b in color_space:
                if a == b:
                    continue
                yield f'mapcolor({a},{b})'


def arc_search(input_grid, output_grid, max_depth=5) -> list[str]:
    """
    Searches for a sequence of transformations to convert the input_grid into
    the output_grid.
    
    Parameters:
    - input_grid: The initial grid that needs to be transformed.
    - output_grid: The target grid to achieve.
    - available_operations: List of primitive operations that can be used to transform the input grid.
    
    Returns:
    - A list of actions that transforms input_grid into output_grid.
    """
    
    # set of all colors present in this problem
    combined_list = [num for row in input_grid for num in row] + [num for row in output_grid for num in row]
    color_space = set(combined_list)

    output_puzzle = ARCPuzzle(output_grid)
    input_puzzle = ARCPuzzle(input_grid)

    Q = [(input_puzzle, 0)] # tuple of (ARCPuzzle, depth_int)
    parent_map = {input_puzzle: None} ## maps a ARCPuzzle to a tuple (ARCPuzzle, action)


    while len(Q) > 0:
        curr_puzzle, depth = Q.pop(0)
        if depth >= max_depth: break
        if curr_puzzle == output_puzzle: break ## sanity check. This line is only necessary if the input_grid == output_grid, which can't happen
        for action in curr_puzzle.legalActions(color_space):
            new_puzzle = curr_puzzle.copy()
            new_puzzle.executeAction(action)

            if new_puzzle in parent_map: continue

            parent_map[new_puzzle] = (curr_puzzle, action)
            Q.append((new_puzzle, depth + 1))
            if new_puzzle == output_puzzle:
                Q.clear() ## breaks outer loop
                break ## breaks inner loop

    ## work backwards to deduce the actions needed to transform input to output
    ## this will return an empty list if the BFS above did not find the output
    curr_puzzle = output_puzzle
    action_list = []
    while curr_puzzle in parent_map and parent_map[curr_puzzle] is not None:
        parent_puzzle, action = parent_map[curr_puzzle]
        action_list.insert(0, action)
        curr_puzzle = parent_puzzle

    return action_list



# Executes the given transformation on a grid and returns a 2D List
def execute_transformation(puzzle, trans):
    if not isinstance(puzzle, ARCPuzzle):
        puzzle = ARCPuzzle(puzzle)
    
    puzzle = puzzle.copy()
    
    for action in trans:
        puzzle.executeAction(action)
    
    return [list(row) for row in puzzle.state]