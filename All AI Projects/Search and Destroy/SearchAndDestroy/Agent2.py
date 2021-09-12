import numpy as np
from Environment import Cell, Environment
from pprint import pprint
import random


class Agents:
    def __init__(self, Environment):
        self.Environment = Environment
        self.MapSize = self.Environment.dimensions

        # initialize a 2D array which represents the grid
        self.initializeMap = [[Cell(j, i) for i in range(self.MapSize)] for j in range(self.MapSize)]
        self.search_count = 0

    def search(self, QueryCell):
        if not self.CellInRange(QueryCell.row, QueryCell.col):
            return
        self.search_count += 1
        # Assign terrain to the cell being queried
        QueryCell.terrain = self.Environment.Map[QueryCell.row][QueryCell.col].terrain
        target = self.Environment.Map[QueryCell.row][QueryCell.col].target
        # checking for the target for the flat terrain terrain
        if QueryCell.terrain == "flat":
            # false negative rate flat terrain = 0.1, so n = 1 only with 0.1 prob
            prob = int(np.random.binomial(1, 0.1, 1))  # false negative rate is 0.1, so prob = 1 only with 0.1 prob
            if (prob != 1 and not target) or (prob == 1):
                # if target is not found or for false negative update the belief states
                self.initializeMap[QueryCell.row][QueryCell.col].belief = 0.1 * QueryCell.belief
                self.initializeMap[QueryCell.row][QueryCell.col].belief2 = 0.9 * QueryCell.belief
                return "failure"
            # found the target
            elif prob != 1 and target:
                print("success")
                return "success"
        # checking for the target for the hilly terrain terrain
        elif QueryCell.terrain == "hilly":
            # false negative rate hilly terrain = 0.3, so n = 1 only with 0.1 prob
            prob = int(np.random.binomial(1, 0.3, 1))
            if (prob != 1 and not target) or (prob == 1):
                self.initializeMap[QueryCell.row][QueryCell.col].belief = 0.3 * QueryCell.belief
                self.initializeMap[QueryCell.row][QueryCell.col].belief2 = 0.7 * QueryCell.belief
                return "failure"
            elif prob != 1 and target:
                print("success")
                return "success"
        # checking for the target for the forest terrain terrain
        elif QueryCell.terrain == "forest":
            # false negative rate forest terrain = 0.7, so n = 1 only with 0.1 prob
            prob = int(np.random.binomial(1, 0.7, 1))
            if (prob != 1 and not target) or (prob == 1):
                self.initializeMap[QueryCell.row][QueryCell.col].belief = 0.7 * QueryCell.belief
                self.initializeMap[QueryCell.row][QueryCell.col].belief2 = 0.3 * QueryCell.belief
                return "failure"
            elif prob != 1 and target:
                print("success")
                return "success"
        # checking for the target for the caves terrain terrain
        elif QueryCell.terrain == "caves":
            # false negative rate forest terrain = 0.9, so n = 1 only with 0.1 prob
            prob = int(np.random.binomial(1, 0.9, 1))
            if (prob != 1 and not target) or (prob == 1):
                self.initializeMap[QueryCell.row][QueryCell.col].belief = 0.9 * QueryCell.belief
                self.initializeMap[QueryCell.row][QueryCell.col].belief2 = 0.1 * QueryCell.belief
                return "failure"
            elif prob != 1 and target:
                print("Found Target!")
                return "success"

    # if the row and col values are in the boundaries

    def CellInRange(self, row: int, col: int):
        return (row >= 0) and (row < self.MapSize) and (col >= 0) and (col < self.MapSize)

    def BasicAgent2(self):
        # Initialize the belief states of the target in a given cell
        for row in range(self.MapSize):
            for col in range(self.MapSize):
                # ex: 50x50 matrix has 1/2500 as the initial belief state
                self.initializeMap[row][col].belief = 1 / (self.MapSize * self.MapSize)
        for row in range(self.MapSize):
            for col in range(self.MapSize):
                if self.Environment.Map[row][col].terrain == "caves":
                    self.initializeMap[row][col].belief2 = 0.1 * self.initializeMap[row][col].belief
                elif self.Environment.Map[row][col].terrain == "forest":
                    self.initializeMap[row][col].belief2 = 0.3 * self.initializeMap[row][col].belief
                elif self.Environment.Map[row][col].terrain == "hilly":
                    self.initializeMap[row][col].belief2 = 0.7 * self.initializeMap[row][col].belief
                elif self.Environment.Map[row][col].terrain == "flat":
                    self.initializeMap[row][col].belief2 = 0.9 * self.initializeMap[row][col].belief
        # initially pick a cell at random
        curr_cell = self.initializeMap[random.randrange(0, len(self.initializeMap))][
            random.randrange(0, len(self.initializeMap))]

        if self.search(curr_cell) == "success":
            return [self.search_count, curr_cell.terrain]

        while 1:
            # given a cell, parse through its neighboring cells
            initialBelief2 = 0
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if not self.CellInRange(curr_cell.row + i, curr_cell.col + j):
                        continue
                    # neighbours of the current cell
                    curr_neighbour = self.initializeMap[curr_cell.row + i][curr_cell.col + j]
                    curr_neighbour.distance = 1 + abs(curr_neighbour.row - self.Environment.target_cell.row) + abs(
                        curr_neighbour.col - self.Environment.target_cell.row)
                    # taking the neighbour cell with the highest belief of where the target is in the cell
                    if curr_neighbour.belief2 > initialBelief2:
                        initialBelief2 = curr_neighbour.belief2
                        next_cell = curr_neighbour
                    elif curr_neighbour.belief2 == initialBelief2 and curr_neighbour.distance < next_cell.distance:
                        # use manhattan distance
                        next_cell = curr_neighbour
            if self.search(next_cell) == "success":
                break
            curr_cell = next_cell
        return [self.search_count, next_cell.terrain]


for j in range(1):
    s = 0
    n = 10  # number of maps to be generated
    dim = 50  # size of map
    for i in range(n):
        env = Environment(dim)
        ab = Agents(env).BasicAgent2()
        print(ab)
        s += ab[0]
    print("Total number of searches: " + str(s))
    print("Average number of searches: " + str(s / n))
