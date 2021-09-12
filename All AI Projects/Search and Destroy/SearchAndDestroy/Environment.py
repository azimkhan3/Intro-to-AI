import random
from pprint import pprint
import numpy as np


class Cell:
    def __init__(self, row, col):
        self.row = row  # instantiate number of rows in the map
        self.col = col  # instantiate number of rows in the map
        self.terrain = None  # instantiate the different terrains "hilly, flat, forested, and maze of caves
        self.target = False  # assign a target to destroy
        self.belief = 0  # instantiate the belief state about where the target is in the cell
        self.belief2 = 0  # instantiate the belief state of finding the target in a cell
        self.distance = 0  # the distance for each cell


class Environment:
    def __init__(self, MapSize):
        self.dimensions = MapSize
        # creating cell objects
        self.Map = [[Cell(j, i) for i in range(self.dimensions)] for j in range(self.dimensions)]
        # generating a Map with terrains and target
        self.InitializeMap()

    def InitializeMap(self):
        self.generate_terrain()
        self.assign_target()

    def generate_terrain(self):
        counter = 0
        # add all of the terrains "hilly, flat, forested, and maze of caves
        flat_count = self.dimensions * self.dimensions * 0.25
        hilly_count = self.dimensions * self.dimensions * 0.25
        forested_count = self.dimensions * self.dimensions * 0.25
        maze_of_caves = self.dimensions * self.dimensions * 0.25

        while counter < flat_count:
            # Choose a random cell from the Map
            row = random.randrange(0, self.dimensions)
            col = random.randrange(0, self.dimensions)
            # Fill empty cells with terrain
            if self.Map[row][col].terrain is None:
                self.Map[row][col].terrain = "flat"
                counter += 1
        counter = 0
        while counter < hilly_count:
            # Choose a random cell from the Map
            row = random.randrange(0, self.dimensions)
            col = random.randrange(0, self.dimensions)
            # Fill empty cells with terrain
            if self.Map[row][col].terrain is None:
                self.Map[row][col].terrain = "hilly"
                counter += 1
        counter = 0
        while counter < forested_count:
            # Choose a random cell from the Map
            row = random.randrange(0, self.dimensions)
            col = random.randrange(0, self.dimensions)
            # Fill empty cells with terrain
            if self.Map[row][col].terrain is None:
                self.Map[row][col].terrain = "forest"
                counter += 1
        # for remaining 25%, fill the cells with maze of caves
        for row in range(self.dimensions):
            for col in range(self.dimensions):
                if self.Map[row][col].terrain is None:
                    self.Map[row][col].terrain = "caves"

    def assign_target(self):
        row = random.randrange(0, self.dimensions)
        col = random.randrange(0, self.dimensions)

        self.target_cell = self.Map[row][col]
        self.Map[row][col].target = True
        print("Target: " + str(row) + ',' + str(col))
