import numpy as np
from numpy import sqrt


# from matplotlib import pyplot as plt

class Node:  # initialize node class
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):  # Node class has two attributes, parent and position
        self.parent = parent
        self.position = position

        self.g = 0  # represents exact cost of path from start node to another node
        self.h = 0  # represents estimated cost from node n to the goal node
        self.f = 0  # lowest cost for the nodes neighbors (where f = g(n) + h(n))

    #
    # def __str__(self) -> str:
    #     return str(self.position)

    def __eq__(self, other):
        return self.position == other.position  # simply compares the positions of two nodes


#
# def aStar(maze, graph, current, end):
#     openList = []
#     closedList = []
#     path = []
#
#     def retracePath(c):
#         path.insert(0,c)
#         if c.parent == None:
#             return
#         retracePath(c.parent)
#
#     openList.append(current)
#     while len(openList) is not 0:
#         current = min(openList, key=lambda inst:inst.H)
#         if current == end:
#             return retracePath(current)
#         openList.remove(current)
#         closedList.append(current)
#         for tile in graph[current]:
#             if tile not in closedList:
#                 tile.H = (abs(end.x-tile.x)+abs(end.y-tile.y))*10
#                 if tile not in openList:
#                     openList.append(tile)
#                 tile.parent = current
#     return path
def manhattan_distance(start, goal):  # heuristic 1
    return abs(start[0] - goal[0]) + abs(start[1] - goal[1])


def diagonal_distance(start, goal):  # heuristic 2
    return max(abs(start[0] - goal[0]), abs(start[1] - goal[1]))


def euclidean_distance(start, goal):  # heuristic 3 -> This is used in A*
    return sqrt((start[0] - goal[0]) ** 2 + (start[1] - goal[1]) ** 2)


def return_path(current_node, maze):  # to be used in A* given a current node and the maze the path is returned if
    # found or if it does not exist
    path = []  # initialize empty path list
    numRows, numCols = np.shape(maze)  # num of rows is equal to num cols as it is a square maze
    result = [[-1 for i in range(numCols)] for j in range(numRows)]  # initialize matrix for result (row,col)
    current = current_node
    while current is not None:
        path.append(current.position)  # put current position in the path list if current has a value
        current = current.parent  # set current equal to its parent(BACKTRACKING)
    path = path[::-1]  # REVERSE path list so it goes from start to goal
    start_value = 0
    for i in range(len(path)):  # parses through length of the path
        result[path[i][0]][path[i][1]] = start_value  # assigns start value at index[row][col]
        start_value += 1
    return result


def astar(maze, cost, start, end):  # given the initial maze, cost heuristic, start and end return a list of tuples as
    # a path

    # initialize start and goal nodes
    startNode = Node(None, tuple(start))
    startNode.g = startNode.h = startNode.f = 0  # there are no heuristics associated with start and goal node as
    # they are static
    goalNode = Node(None, tuple(end))
    goalNode.g = goalNode.h = goalNode.f = 0

    # Initialize both frontier and explored list
    frontierList = []  # list of possible open nodes
    exploredList = []  # list of nodes that follow the path

    # Add the start node to the frontier list
    frontierList.append(startNode)

    outer_iteration = 0
    max_iteration = (len(maze) // 2) ** 10

    numRows, numCols = np.shape(maze)  # square matrix, so numRows = numCols = shape of maze (numpy function)
    # Loop until you find the end
    while len(frontierList) > 0:  # there are still open nodes to be explored
        outer_iteration += 1
        # Get the current node
        current_node = frontierList[0]
        current_index = 0  # set current nodes index to 0

        # enumerate function returns index and value of the key frontier list
        for index, value in enumerate(frontierList):  # store list index location in index and list value in value
            if value.f < current_node.f:  # if cost of the key in the frontier list is less than cost of the current
                # node
                current_node = value  # make value the new current node
                current_index = index  # make the index the new current index

        if outer_iteration > max_iteration:
            print("No solution or heuristic cost is too high")
            return return_path(current_node, maze)  # terminates while loop and returns the path

        # Pop current off frontier list, append to the explored list
        frontierList.pop(current_index)
        exploredList.append(current_node)

        # Found the goal
        if current_node == goalNode:
            return return_path(current_node, maze), len(exploredList) + 1  # return the path as well as the number of
            # nodes expanded

        # Generate children as an empty list
        children = []
        canMove = [[-1, 0], [0, -1], [1, 0], [0, 1]]  # path can only move up, down, left, and right one square block
        for new_position in canMove:  # Adjacent square blocks... new position is a list of positions

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range of the canvas of the whole maze
            if node_position[0] > (numRows - 1) or node_position[0] < 0 or node_position[1] > (numCols - 1) or \
                    node_position[1] < 0:
                continue  # continue goes to the next iteration in the for loop, exiting the if statement

            # the maze should only path through open cells
            if maze[node_position[0]][node_position[1]] != 0:
                continue  # continue goes to the next iteration in the for loop, exiting the if statement

            # Create new node
            new_node = Node(current_node, node_position)  # the current node is the parent and the node position is the
            # position

            # Append the new node to children list
            children.append(new_node)
        # CHILDREN SHOULD HAVE A LIST OF POSSIBLE NODE LOCATIONS WHEN IT EXITS THIS FOR LOOP

        # Loop through children
        for child in children:

            # Child is on the explored list
            # if children in exploredList:
            #     continue
            if len([closed_child for closed_child in exploredList if closed_child == child]) > 0:
                continue

            # for closed_child in exploredList:
            #     if closed_child == child:
            #         continue

            # Create the f, g, and h values
            child.g = current_node.g + cost  # represents exact cost of path from start node to another node
            # child.h = euclidean_distance(start=child.position, goal=goalNode.position)

            # heuristic used for child h is euclidean right now
            child.h = ((child.position[0] - goalNode.position[0]) ** 2) + (
                    (child.position[1] - goalNode.position[1]) ** 2)  # represents estimated cost from node n to the
            # goal node
            child.f = child.g + child.h  # total cost (exact + estimated cost)

            if len([i for i in frontierList if child == i and child.g > i.g]) > 0:  #
                continue
            # Child is already in the open list
            # for open_node in frontierList:
            #     if child == open_node and child.g > open_node.g:
            #         continue
            # for open_node in frontierList:
            #     if child == open_node and child.g > open_node.g:
            #         should_pass = True
            #
            #         if should_pass:continue

            # Add the child to the open list
            frontierList.append(child)


def main():
    maze = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 1, 0, 1, 0],
            [0, 0, 0, 0, 1, 0, 1, 0, 1, 0],
            [0, 0, 0, 0, 1, 0, 1, 0, 1, 0],
            [0, 0, 0, 0, 1, 0, 1, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
            [0, 0, 0, 0, 1, 0, 1, 0, 1, 0],
            [0, 0, 0, 0, 1, 0, 1, 0, 1, 0],
            [0, 0, 0, 0, 1, 0, 1, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    start = (0, 0)
    end = (9, 9)
    cost = 1
    path = astar(maze, cost, start, end)
    print(path)


#
def dfs_path(graph: dict, start: tuple, end: tuple):  # driver for dfs
    visited = []
    visited = dfs(start, graph, visited)
    if end in visited:
        print("Path found")
        return visited
    else:
        print("Path not found")


def dfs(node, graph, visited):  # depth first search algorithm
    visited.append(node)
    for neighbor in graph[node]:  # looks at every neighbor for one given node
        if not neighbor in visited:  # recursive statement runs dfs for every node that has not been visited yet
            dfs(neighbor, graph, visited)  # every time looks at neighbor of the current node
    return visited


# Driver Code for breadth first search
def bfs_path(graph, start, goal):
    explored = []

    # Queue for traversing the
    # graph in the BFS
    queue = [[start]]

    # If the desired node is
    # reached
    if start == goal:
        print("Same Node")
        return

    # Loop to traverse the graph
    # with the help of the queue
    while queue:
        path = queue.pop(0)
        node = path[-1]

        # Condition to check if the
        # current node is not visited
        if node not in explored:
            neighbours = graph[node]

            # Loop to iterate over the
            # neighbours of the node
            for neighbour in neighbours:
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)

                # Condition to check if the
                # neighbour node is the goal
                if neighbour == goal:
                    # print("Shortest path BFS = ", *new_path)
                    return new_path
            explored.append(node)

    # Condition when the nodes
    # are not connected
    print("So sorry, but a connecting path doesn't exist :(")

    return

    # #m = Maze(rows=6, cols = 6, p=.3, on_fire=False, q=.3)

    # path = BFS_SP(m.graph, (0,0), (m.rows-1,m.cols-1))
    # print(path)

    # x = m.maze
    # x[0][0] = 0
    # x[m.rows-1][m.cols-1] = 0

    # path = astar(x, (0,0), (m.rows-1,m.cols-1))

    # print(path)

# graph = {
#     'A' : ['B','C'],
#     'B' : ['D', 'E'],
#     'C' : ['F'],
#     'D' : [],
#     'E' : ['F'],
#     'F' : []
# }
# graph2 = {'A': ['B', 'E', 'C'], 
#         'B': ['A', 'D', 'E'], 
#         'C': ['A', 'F', 'G'], 
#         'D': ['B', 'E'], 
#         'E': ['A', 'B', 'D'], 
#         'F': ['C'], 
#         'G': ['C']}
