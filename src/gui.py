import tkinter as tk
from tkinter import messagebox

from game import MazeGame
from grid import LEVELS, grid_from_lines

CELL_SIZE = 40


class MazeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Navigator")

        self.level_number = "1"
        self.game = MazeGame(grid_from_lines(LEVELS[self.level_number]))

        self.canvas = tk.Canvas(root)
        self.canvas.pack()

        frame = tk.Frame(root)
        frame.pack()

        tk.Button(frame, text="Level 1", command=lambda: self.change_level("1")).pack(side=tk.LEFT)
        tk.Button(frame, text="Level 2", command=lambda: self.change_level("2")).pack(side=tk.LEFT)
        tk.Button(frame, text="Level 3", command=lambda: self.change_level("3")).pack(side=tk.LEFT)
        tk.Button(frame, text="Show Path", command=self.show_path).pack(side=tk.LEFT)

        self.root.bind("<Key>", self.handle_key)

        self.draw_grid()

    def change_level(self, level_number):
        self.level_number = level_number
        self.game = MazeGame(grid_from_lines(LEVELS[level_number]))
        self.draw_grid()

    def show_path(self):
        self.game.calculate_path()
        self.draw_grid()

        if self.game.won:
            messagebox.showinfo("Victory!", "You reached the goal!")

    def handle_key(self, event):
        key = event.char.lower()

        if key in ["w", "a", "s", "d"]:
            self.game.move(key)
            self.draw_grid()

            if self.game.won:
                messagebox.showinfo("Victory!", "You reached the goal!")

    def draw_grid(self):
        self.canvas.delete("all")

        rows = len(self.game.grid)
        cols = len(self.game.grid[0])

        self.canvas.config(width=cols * CELL_SIZE, height=rows * CELL_SIZE)

        for r in range(rows):
            for c in range(cols):
                x1 = c * CELL_SIZE
                y1 = r * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE

                cell = self.game.grid[r][c]

                color = "white"
                if cell == "#":
                    color = "black"
                elif cell == "S":
                    color = "green"
                elif cell == "G":
                    color = "red"

                if self.game.current_path and (r, c) in self.game.current_path:
                    color = "yellow"

                if (r, c) == self.game.player:
                    color = "blue"

                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color,
                    outline="gray"
                )


if __name__ == "__main__":
    root = tk.Tk()
    app = MazeGUI(root)
    root.mainloop()