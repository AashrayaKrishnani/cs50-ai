import sys

class Node:
    def __init__(self, state, parent, action, cost=None, steps=0):
        self.state = state
        self.action = action
        self.parent = parent
        self.cost = cost
        self.steps = steps

class Frontier:
    def __init__(self) :
        self.frontier = []
    def add(self, node):
        self.frontier.append(node)
    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)
    def isEmpty(self):
        return len(self.frontier) == 0
    def get(self):
        raise NotImplementedError('Implement this dude!')

class StackFrontier(Frontier):      # That means it inherits from Frontier
    def get(self):
        if len(self.frontier) == 0:
            raise Exception('Frontier empty')
        else:
            return self.frontier.pop()  # By default removes the last element.

class QueueFrontier(Frontier):
    def get(self):
        if len(self.frontier) == 0:
            raise Exception('Frontier empty')
        else:
            return self.frontier.pop(0)

class ModifiedQueueFrontier(QueueFrontier):
    def get(self):
        if len(self.frontier) == 0:
            raise Exception('Frontier empty')
        else:
            least_cost_index = 0

            for node in self.frontier:
                if node.cost < self.frontier[least_cost_index].cost:
                    least_cost_index = self.frontier.index(node)

            return self.frontier.pop(least_cost_index)        

class AstarFrontier(QueueFrontier):
    def get(self):
        if len(self.frontier) == 0:
            raise Exception('Frontier empty')
        else:
            least_netCost_index = 0
            for node in self.frontier:
                if (node.cost + node.steps) < (self.frontier[least_netCost_index].cost + self.frontier[least_netCost_index].steps):
                    least_netCost_index = self.frontier.index(node)

            return self.frontier.pop(least_netCost_index)    


class Maze:
    def __init__(self, filename, show_explored=False):
        
        # Loading Maze from file
        with open(filename) as f:
            contents = f.read()
        
        if contents.count('A')  != 1:
            raise Exception('There must be only 1 instance of \'A\'')
        if contents.count('B')  != 1:
            raise Exception('There must be only 1 instance of \'B\'')

        contents = contents.splitlines()

        # Determining heigth and width
        self.height = len(contents)
        self.width = max(len(row) for row in contents)

        # Keeping track of walls
        self.walls = []

        for i in range(self.height):
            wall = []
            for j in range(self.width):
                try:
                    if contents[i][j] == 'A':
                        self.start = (i,j)
                    elif contents[i][j] == 'B':
                        self.goal = (i,j)
                    
                    wall.append(contents[i][j]=='#')
                except IndexError:
                    wall.append(False)
            self.walls.append(wall)

        self.solution = None
        self.show_explored = show_explored
        self.explored = set()

    def neighbours(self, state):
        row, col = state

        candidates = [ ("Up", (row-1, col)),
        ("Left", (row, col-1)),
        ("Right", (row, col+1)),
        ("Down", (row+1, col))]

        result=[]

        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r,c)))
        return result


    def solve(self):

        # To Keep track of states explored
        self.states_explored = 0

        start = Node(state=self.start, parent=None, action=None, cost=self.cost(self.start))
        frontier = ModifiedQueueFrontier()      # Use StackFrontier = DFS, QueueFrontier = BFS, ModifiedQueueFrontier = G-BFS, AstarFrontier = AstarFrontier 
        frontier.add(start)

        # To avoid loops from revisiting previously explored nodes.
        self.explored = set()

        while(True):

            # If frontier is empty
            if frontier.isEmpty():
                raise Exception('No solution')

            # Getting a node from the frontier to evaluate
            node = frontier.get()
            self.states_explored += 1

            # if it's the goal, then voila!
            if node.state == self.goal:
                actions = []
                cells = []

                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                cells.reverse()
                actions.reverse()
                self.solution = (actions, cells)
                return
            else:
                # Mark it as explored
                self.explored.add(node.state)
                # Adding neighbours to frontier
                for action, state in self.neighbours(node.state):
                    if not frontier.contains_state(state) and state not in self.explored:
                        child = Node(state = state, parent = node, action = action, cost = self.cost(state), steps = node.steps+1)
                        frontier.add(child)

    def cost(self, state):
        manh_dist = abs(state[0] - self.goal[0]) + abs(state[1] - self.goal[1])
        return manh_dist
        


    def print(self):
        # Getting the list of 'cells' from the soltion pair of (actions, cells)
        solution = self.solution[1] if self.solution != None else None

        print()

        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end='')  # If there's a wall.
                elif (i,j) == self.start:
                    print("A", end='')
                elif (i,j) == self.goal:
                    print("B", end='')
                elif solution is not None and (i,j) in solution:
                    print("*", end='')
                elif self.show_explored and (i,j) in self.explored:
                    print('X', end='')
                else:
                    print(" ", end='')  # Empty Path :D

            print()
        print()

        
if len(sys.argv) != 2:
    sys.exit("Usage: python maze.py maze.txt")


maze = Maze(sys.argv[1], show_explored=True)

print("Here's the Maze:")
maze.print()

print("Solving...")
maze.solve()
print("Solved.")
print()
print("States explored = " + str(maze.states_explored ), end='\n\n')

print("Solution:")
maze.print()

