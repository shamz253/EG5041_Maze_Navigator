"""Shortest-path search for the Maze Navigator game."""
from __future__ import annotations

from collections import deque

from grid import Grid, Position, neighbours


def find_path(grid: Grid, start: Position, goal: Position) -> list[Position]:
    """Return a shortest path from start to goal using Breadth-First Search.

    BFS is appropriate because every move on this grid has equal cost. It explores
    cells by distance from the start, so the first time it reaches the goal it has
    found a path with the fewest number of steps.
    """
    if start == goal:
        return [start]

    frontier = deque([start])
    came_from: dict[Position, Position | None] = {start: None}

    while frontier:
        current = frontier.popleft()
        for next_position in neighbours(grid, current):
            if next_position in came_from:
                continue
            came_from[next_position] = current
            if next_position == goal:
                return reconstruct_path(came_from, goal)
            frontier.append(next_position)

    return []


def reconstruct_path(came_from: dict[Position, Position | None], goal: Position) -> list[Position]:
    """Build an ordered path by walking backwards from the goal to the start."""
    path: list[Position] = []
    current: Position | None = goal

    while current is not None:
        path.append(current)
        current = came_from[current]

    path.reverse()
    return path
