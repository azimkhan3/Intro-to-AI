import numpy as np
import random


class Maze:

    def __init__(self, rows: int = 10, cols: int = 10, p=.3) -> None:
        self.position = (0, 0)  # initialize starting position
        self.p = p  # initialize obstacle density p
        self.rows = rows  # initialize rows
        self.cols = cols  # initialize columns
        self.generate_maze(self.rows, self.cols, self.p)  # initialize maze generation from function below
        self.set_adjacency_ll()  # initialize adjacency linked list, which stores the nieghbors

    def generate_maze(self, rows, cols, p):
        # 0 = empty
        # 1 = wall
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

        # reset start and goal positions
        self.maze[0][0] = 0
        self.maze[rows - 1][cols - 1] = 0

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
