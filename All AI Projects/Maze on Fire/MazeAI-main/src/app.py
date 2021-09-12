import tkinter as tk
from tkinter import messagebox
from firemaze import advance_fire_onestep, Maze, take_step, strat_2, strat_3
import numpy

# Initialize GUI
def create(maze):
    for row in range(maze.rows):
        for col in range(maze.cols):
            if maze.maze[row][col] == 0: # All open cells are white
                color = 'White'
            elif maze.maze[row][col] == 1: # All obstacle cells are black
                color = 'black'
            elif maze.maze[row][col] == 2: # The start cell is purple
                color = 'purple'
            elif maze.maze[row][col] == 3: # The goal cell is green
                color = 'green'
            elif maze.maze[row][col] == 4: # The initial fire cell is red
                color = 'red'
            draw(row, col, color)

    for spot in maze.path:
        print(maze.position == spot)
        if spot != maze.position and spot != (maze.rows - 1, maze.cols - 1):
            draw(spot[0], spot[1], "yellow") # HIGHLIGHT PATH IN YELLOW


def check_you_dead():
    print(maze)

    if maze.maze[maze.position[0]][maze.position[1]] == 4:
        messagebox.showerror("Title", "Agent has died or is about to die")
        print("YOU ARE DEAD")
        return True
    elif not maze.path_exists:
        messagebox.showerror("Title", "Agent has died or is about to die")
        print("AGENT IS DEAD")
        return True
    return False


def draw(row, col, color):
    x1 = col * cell_size
    y1 = row * cell_size
    x2 = x1 + cell_size
    y2 = y1 + cell_size
    ffs.create_rectangle(x1, y1, x2, y2, fill=color) # create maze


def spead_fire(): # SPREADS FIRE
    advance_fire_onestep(maze) # CALL ADVANCE FIRE ONE STEP
    # print(m)
    for fire in maze.fire_spots:
        draw(fire[0], fire[1], "red") # MAKE CELL A FIRE CELL FOR EVERY FIRE IN MAZE.FIRE_SPOTS


# def spead_water():
#     advance_water_onestep(maze)
#     # print(m)
#     for water in maze.water_spots:
#         draw(water[0], water[1], "blue")


def move():
    # if m == False:
    #     tk.messagebox.showerror("Title", "YOU DEAD OR U BOUTA DIE")

    draw(maze.position[0], maze.position[1], "white")
    # print(m)
    if strat == 1:
        print("1")
        m = take_step(maze)
    elif strat == 2:
        print("2")
        m = strat_2(maze)
    else:
        m = strat_3(maze)

    if (m == None):
        messagebox.showerror("Title", "No Path exists")

    print(maze.position)
    draw(maze.position[0], maze.position[1], "purple")
    spead_fire()
    # spead_water()
    if check_you_dead():
        return
    create(maze)


strat = 1

# when a strategy is picked, the other strategy buttons are destroyed
def set_strategy(value):
    global strat
    strat = value
    strat1_but.destroy()
    strat2_but.destroy()
    strat3_but.destroy()


if __name__ == "__main__":
    while (1):
        maze = Maze(rows=20, cols=20, p=.2, on_fire=True, q=.2)
        if (maze.path_exists):
            break
    # while not maze.path_exists:
    #     print(maze)
    #     maze = Maze(rows=12, cols = 12, p=.2, on_fire=True, q=.3)

    # print(maze.path)
    cell_size = 30

    window = tk.Tk()
    window.title('Maze')

    row_size = cell_size * maze.rows
    col_size = cell_size * maze.cols
    ffs = tk.Canvas(window, width=col_size, height=row_size, bg='grey')
    ffs.pack()

    ffs.grid(row=0, column=0)

    advance_fire_button = tk.Button(window, text="click to spread fire", command=move)
    strat1_but = tk.Button(window, text="Strategy 1", command=lambda *args: set_strategy(1))
    strat2_but = tk.Button(window, text="Strategy 2", command=lambda *args: set_strategy(2))
    strat3_but = tk.Button(window, text="Strategy 3", command=lambda *args: set_strategy(2))
    advance_fire_button.grid(row=1, column=0)

    strat1_but.grid(row=2, column=0)
    strat2_but.grid(row=3, column=0)
    strat3_but.grid(row=4, column=0)
    create(maze)

    # draw(scr, scc, start_color)

    window.mainloop()
