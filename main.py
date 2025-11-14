"""
JungleQuest Game - Main Entry Point

This module serves as the entry point for the JungleQuest game application.
It initializes the game controller and starts the game loop.
"""

from controller.controller import Controller


def main() -> None:
    """
    Initialize and start the JungleQuest game.

    Creates a Controller instance and begins the game session,
    including player setup and main game loop.
    """
    controller = Controller()
    controller.start_game()


if __name__ == "__main__":
    main()
