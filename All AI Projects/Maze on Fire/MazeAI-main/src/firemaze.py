import numpy as np
import random
import search
import time


# AGENT TAKES ONE STEP IN GUI (Essentially Strat 1)
def take_step(maze):
    x = maze.path

    if x == None:
        return False
    step = x.pop(0)
    if step == maze.position:
        step = x.pop(0)
    maze.fire_maze[maze.position[0]][maze.position[1]] = 0
    maze.fire_maze[step[0]][step[1]] = 2
    maze.position = step
    return maze


# Strategy 2: Calculates an optimal path everytime it takes a step, avoiding fires unless no other path available
def strat_2(maze):
    take_step(maze)
    maze.get_path()
    return maze


# Strategy 3: Calculates an optimal path by looking at the distance from the current position to closest fire.
# If the fire distance (fire pos - curr pos) is less than 5 blocks, use BFS. Else use A*
def strat_3(maze):
    # implement logic
    take_step(maze)
    return maze


# ADVANCES FIRE RANDOMLY ONE STEP
def advance_fire_onestep(maze):
    m = maze
    # print(m)
    new_fires = []  # keep track of a list of neighbors for a current node

    for node in maze.graph.keys():
        # KEEP TRACK OF NEIGHBORS
        k = 0

        # up neighbor
        if (((node[0] - 1), node[1]) not in new_fires and (node[0] - 1 >= 0)
                and ((node[0] - 1), node[1]) in maze.fire_spots):
            k += 1
        # down neighbor
        if (((node[0] + 1), node[1]) not in new_fires and (node[0] + 1 <= maze.rows)
                and ((node[0] + 1), node[1]) in maze.fire_spots):
            k += 1
        # left neighbor
        if ((node[0], (node[1] - 1)) not in new_fires and (node[1] - 1 >= 0)
                and (node[0], (node[1] - 1)) in maze.fire_spots):
            k += 1
        # right neighbor
        if ((node[0], (node[1] + 1)) not in new_fires and (node[1] + 1 <= maze.cols)
                and (node[0], (node[1] + 1)) in maze.fire_spots):
            k += 1

        prob = 1 - pow(float((1 - maze.q)), float(k))  # probability equation

        if random.random() <= prob:  # if random is less than or equal to the probability
            new_fires.append(node)  # append current node to new fires list

            m.fire_maze[node[0]][node[1]] = 4  # set position of current cell as a fire cell in the maze

            m.fire_spots.append(node)  # appends node to the maze's fire spots

    for fire in new_fires:
        m.graph.pop(fire)

    m.set_adjacency_ll()

    return m


# SAME as Maze class in Maze.py except we incorporated fires
class Maze:

    def __init__(self, rows: int = 10, cols: int = 10, p=.3, on_fire=False, q=.3) -> None:
        self.position = (0, 0)  # starting position
        self.p = p  # initialize obstacle density p
        self.fire = on_fire  # initialize fire
        self.rows = rows  # initialize rows
        self.cols = cols  # initialize columns
        self.generate_maze(self.rows, self.cols, self.p)
        self.set_adjacency_ll()
        self.fire_spots = []
        if (on_fire):
            self.start_fire()
            self.q = q
            self.fire_maze = self.maze  # maze we will update based on fire

        self.check_path_exists()
        if self.path_exists:
            self.get_path()

    def check_win(self):
        return True if self.position == (self.rows - 1, self.cols - 1) else False

    def get_path(self):
        self.path = search.bfs_path(self.graph, self.position, ((self.rows - 1), (self.cols - 1)))

    def check_path_exists(self):
        self.path_exists = search.dfs_path(self.graph, self.position, ((self.rows - 1), (self.cols - 1)))
        # print(self.path_exists)

    def generate_maze(self, rows, cols, p):
        # 0 = empty
        # 1 = wall
        # 2 = user
        # 3 = finish
        # 4 = fire
        self.graph = {}  # initialize empty graph
        self.maze = np.zeros((rows, cols))  # initialize maze matrix with all 0s (essentially empty cell maze)
        self.graph[(0, 0)] = []
        # goes through each row and column position. place obstacles randomly at a given [row][col] based on p value
        for r in range(rows):
            for c in range(cols):
                if random.random() < p:
                    self.maze[r][c] = 1
                else:
                    self.graph[(r, c)] = []  # if random greater than p, do nothing
        self.graph[(rows - 1, cols - 1)] = []

        self.maze[0][0] = 2
        self.maze[rows - 1][cols - 1] = 3

    # FIND NEIGHBORS
    def set_adjacency_ll(self):
        for key in self.graph.keys():

            neighbors = []  # INITIALIZE A LIST OF NEIGHBORS(EMPTY AT FIRST)
            # up neighbor
            if (key[0] - 1 >= 0) and ((key[0] - 1), key[1]) in self.graph:
                neighbors.append(((key[0] - 1), key[1]))

            # down neighbor
            if (key[0] + 1 <= self.rows) and ((key[0] + 1), key[1]) in self.graph:
                neighbors.append(((key[0] + 1), key[1]))

            # left neighbor
            if (key[1] - 1 >= 0) and (key[0], (key[1] - 1)) in self.graph:
                neighbors.append(((key[0]), key[1] - 1))

            # right neighbor
            if (key[1] + 1 <= self.cols) and (key[0], (key[1] + 1)) in self.graph:
                neighbors.append(((key[0]), key[1] + 1))

            self.graph[key] = neighbors

    # randomly start fire at a location in the maze and initialize cell as a fire cell
    def start_fire(self):
        fire_start = random.choice(list(self.graph.keys()))
        self.maze[fire_start[0]][fire_start[1]] = 4
        self.graph.pop(fire_start)
        self.fire_spots.append(fire_start)  # append the fire start into the fire spots list
        self.set_adjacency_ll()

    def path_exists(self):
        visited = search.dfs((0, 0), self.graph, {key: False for key in self.graph.keys()})
        return True if (visited[(self.rows - 1, self.cols - 1)]) else False

    def __str__(self) -> str:
        return "{}{}".format(self.path_exists, self.fire_spots)


# Driver for the DFS Method (we are testing with size = 60 however this can be changed)
def dfs_test():
    try:
        size = 60
        m = Maze(size, size, p=.3)
        while (not m.path_exists):
            m = Maze(size, size, p=.3)
        start = 0;
        end = 0
        while (end - start < 60):
            m = Maze(size, size, p=.3)
            while (not m.path_exists):
                m = Maze(size, size, p=.3)
            start = time.perf_counter()
            m.check_path_exists()
            end = time.perf_counter()

            size += 1
    except RecursionError:
        print(size)

    print(size)

# MAIN METHOD
if __name__ == "__main__":
    dfs_test()
