"""Terminal version of Maze Navigator for testing the core game logic."""
from __future__ import annotations

import argparse

from game import MazeGame
from grid import LEVELS, grid_from_lines, load_grid, render_grid


def run_text_game(level_path: str | None = None) -> None:
    # If a file path is provided, load from file
    if level_path:
        game = MazeGame(load_grid(level_path))
    else:
        # Level selection menu
        print("Choose a level:")
        print("1 = Easy")
        print("2 = Medium")
        print("3 = Hard")

        choice = input("Enter level number: ")

        if choice not in LEVELS:
            print("Invalid choice. Defaulting to Level 1")
            choice = "1"

        selected_level = LEVELS[choice]

        # Convert list of strings into grid
        game = MazeGame(grid_from_lines(selected_level))

    print("Maze Navigator - text mode")
    print("Commands: w/a/s/d move, p show shortest path, r reset, q quit")

    while True:
        print("\n" + render_grid(game.grid, game.player, game.current_path))

        if game.won:
            print("You reached the goal. You win!")
            return

        command = input("Command: ").strip().lower()

        if command == "q":
            print("Goodbye.")
            return
        elif command == "p":
            path = game.calculate_path()
            if path:
                print(f"Shortest path length: {len(path) - 1} steps")
            else:
                print("No path exists.")
        elif command == "r":
            game.reset()
        else:
            game.move(command)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Maze Navigator in text mode.")
    parser.add_argument("--level", help="Optional path to a level text file.")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_text_game(args.level)