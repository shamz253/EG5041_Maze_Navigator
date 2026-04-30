"""Grid loading and movement rules for the Maze Navigator game."""
from __future__ import annotations

from pathlib import Path
from typing import List, Tuple

Position = Tuple[int, int]
Grid = List[List[str]]

WALL = "#"
FLOOR = "."
START = "S"
GOAL = "G"

LEVEL_1 = [
    "##########",
    "#S.......#",
    "#.#####..#",
    "#.....#..#",
    "#.###.#..#",
    "#...#.#..#",
    "###.#.####",
    "#...#....#",
    "#.#####G##",
    "##########",
]

LEVEL_2 = [
    "##########",
    "#S.......#",
    "####.###.#",
    "#....#...#",
    "#.####.#.#",
    "#......#G#",
    "##########",
]

LEVEL_3 = [
    "############",
    "#S.....#...#",
    "#.###.#.#..#",
    "#...#.#.#..#",
    "###.#.#.##.#",
    "#...#......#",
    "#.#######.##",
    "#.........G#",
    "############",
]
LEVELS = {
    "1": LEVEL_1,
    "2": LEVEL_2,
    "3": LEVEL_3,
}
# This is the one your game will use
DEFAULT_LEVEL = LEVEL_1


def grid_from_lines(lines: list[str]) -> Grid:
    """Convert text lines to a rectangular list-of-lists grid and validate it."""
    cleaned = [line.strip() for line in lines if line.strip()]
    if not cleaned:
        raise ValueError("Level is empty.")

    width = len(cleaned[0])
    if any(len(row) != width for row in cleaned):
        raise ValueError("All level rows must have the same length.")

    allowed = {WALL, FLOOR, START, GOAL}
    grid = [list(row) for row in cleaned]
    invalid = sorted({cell for row in grid for cell in row if cell not in allowed})
    if invalid:
        raise ValueError(f"Invalid cell character(s): {invalid}")

    find_start_and_goal(grid)  # validates exactly one S and one G
    return grid


def load_grid(path: str | Path | None = None) -> Grid:
    """Load a level from a text file, or return the built-in default level."""
    if path is None:
        return grid_from_lines(DEFAULT_LEVEL)
    return grid_from_lines(Path(path).read_text(encoding="utf-8").splitlines())


def find_start_and_goal(grid: Grid) -> tuple[Position, Position]:
    """Return the start and goal positions, requiring exactly one of each."""
    starts: list[Position] = []
    goals: list[Position] = []

    for row_index, row in enumerate(grid):
        for col_index, cell in enumerate(row):
            if cell == START:
                starts.append((row_index, col_index))
            elif cell == GOAL:
                goals.append((row_index, col_index))

    if len(starts) != 1 or len(goals) != 1:
        raise ValueError("A valid level must contain exactly one S and exactly one G.")
    return starts[0], goals[0]


def in_bounds(grid: Grid, position: Position) -> bool:
    """Return True if position is inside the grid."""
    row, col = position
    return 0 <= row < len(grid) and 0 <= col < len(grid[0])


def is_walkable(grid: Grid, position: Position) -> bool:
    """Return True if the position can be occupied by the player."""
    return in_bounds(grid, position) and grid[position[0]][position[1]] != WALL


def neighbours(grid: Grid, position: Position) -> list[Position]:
    """Return valid 4-connected neighbours: up, down, left, right."""
    row, col = position
    candidates = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
    return [candidate for candidate in candidates if is_walkable(grid, candidate)]


def move_player(grid: Grid, player: Position, command: str) -> Position:
    """Move the player for WASD input. Invalid moves leave the player in place."""
    deltas = {
        "w": (-1, 0),
        "s": (1, 0),
        "a": (0, -1),
        "d": (0, 1),
    }
    if command.lower() not in deltas:
        return player

    row_delta, col_delta = deltas[command.lower()]
    next_position = (player[0] + row_delta, player[1] + col_delta)
    return next_position if is_walkable(grid, next_position) else player


def render_grid(grid: Grid, player: Position, path: list[Position] | None = None) -> str:
    """Return a text version of the grid with P and optional path markers overlaid."""
    path_cells = set(path or [])
    lines: list[str] = []

    for row_index, row in enumerate(grid):
        rendered_row = []
        for col_index, cell in enumerate(row):
            position = (row_index, col_index)
            if position == player:
                rendered_row.append("P")
            elif position in path_cells and cell not in {START, GOAL}:
                rendered_row.append("o")
            else:
                rendered_row.append(cell)
        lines.append("".join(rendered_row))

    return "\n".join(lines)
