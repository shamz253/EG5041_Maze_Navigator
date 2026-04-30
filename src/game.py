"""Core game state class used by both the terminal UI and the tkinter GUI."""
from __future__ import annotations

from grid import Grid, Position, find_start_and_goal, move_player
from pathfinding import find_path


class MazeGame:
    """Stores one consistent game state shared by all interfaces."""

    def __init__(self, grid: Grid):
        self.grid = grid
        self.start, self.goal = find_start_and_goal(grid)
        self.player = self.start
        self.current_path: list[Position] = []
        self.won = False

    def move(self, command: str) -> bool:
        """Move the player. Return True when the position changes."""
        if self.won:
            return False

        old_position = self.player
        self.player = move_player(self.grid, self.player, command)
        self.current_path = []
        self.won = self.player == self.goal
        return self.player != old_position

    def calculate_path(self) -> list[Position]:
        """Find and store a shortest path from the current player position to the goal."""
        self.current_path = find_path(self.grid, self.player, self.goal)
        return self.current_path

    def reset(self) -> None:
        """Return the game to the starting state."""
        self.player = self.start
        self.current_path = []
        self.won = False
