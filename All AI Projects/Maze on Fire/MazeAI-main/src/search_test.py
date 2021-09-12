from maze import Maze
from search import astar, bfs_path, dfs_path

import time


if __name__ == '__main__':
    m = Maze(rows=20, cols=20, p=.3)
    print(m.maze)

    # TEST DFS

    # path_exists = dfs_path(m.graph, (0, 0), (m.rows - 1, m.cols - 1))
    # print("dfs path: ")
    # print(path_exists)
    #     print("--- %s seconds ---" % (time.time() - start_time))
        #start_time = time.time()

    # TEST BFS

    # path = bfs_path(m.graph, (0, 0), (m.rows - 1, m.cols - 1))
    # print("bfs path: ")
    # print(path)

        #print("--- %s seconds ---" % (time.time() - start_time))

    # TEST ASTAR

    cost = 1
    astarpath = astar(m.maze, cost, (0,0), (m.rows-1, m.cols-1))
    print("astar path: ")
    print(astarpath)



