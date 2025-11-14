"""
View Module

This module contains the View class responsible for all display
and user input operations.
"""

from typing import Dict
from model.board import Board
from model.tile import Tile


class View:
    """
    Handles all display and input operations for the game.

    Attributes:
        PIECE_ABBREV: Dictionary mapping piece names to abbreviations
        TILE_SYMBOLS: Dictionary mapping tile types to display symbols
    """

    # Piece abbreviations for display
    PIECE_ABBREV: Dict[str, str] = {
        "Rat": "rat",
        "Cat": "cat",
        "Dog": "dog",
        "Wolf": "wlf",
        "Leopard": "lpd",
        "Tiger": "tgr",
        "Lion": "lio",
        "Elephant": "elp",
    }

    # Tile symbols for display
    TILE_SYMBOLS: Dict[str, str] = {
        "L": "  ",
        "D1": "D1",
        "D2": "D2",
        "T": "TR",
        "W": "~~",
    }

    def display_board(self, board: Board) -> None:
        """
        Display the current state of the game board.

        Shows a formatted grid with column labels (A-G), row numbers (1-9),
        pieces with their owners, and special tiles.

        Args:
            board: The Board object to display
        """
        print("\n" + "=" * 60)
        print(" " * 20 + "JUNGLE QUEST")
        print("=" * 60)

        self._print_column_headers()
        print("   +" + "------+" * 7)

        for i in range(board.MAX_ROWS):
            print(f" {i + 1} |", end="")
            for j in range(board.MAX_COLUMNS):
                print(f"{self._format_tile(board.grid[j][i])}|", end="")
            print(f" {i + 1}")
            print("   +" + "------+" * 7)

        self._print_column_headers()
        print("\n" + "=" * 60)

    def _print_column_headers(self) -> None:
        """Print column headers (A-G) for the board."""
        print("    ", end="")
        for col in "ABCDEFG":
            print(f" {col:^6}", end="")
        print()

    def _format_tile(self, tile: Tile) -> str:
        """
        Format a tile for display.

        Args:
            tile: The Tile to format

        Returns:
            Formatted string for display (6 characters wide)
        """
        if not tile.is_empty():
            piece = tile.piece
            abbr = self.PIECE_ABBREV.get(piece.name, piece.name[0])
            piece_str = f"{abbr}{piece.owner + 1}"
            return f"{piece_str:^6}"
        return f"{self.TILE_SYMBOLS.get(tile.tile_type, tile.tile_type):^6}"

    def display_turn(self, player_name: str) -> None:
        """
        Display whose turn it is and game instructions.

        Args:
            player_name: Name of the current player
        """
        print(f"\n>>> Current turn: {player_name}")
        print("Pieces: R=rat, C=cat, D=dog, W=wlf, P=lpd, T=tgr, L=lio, E=elp")
        print("Tiles: D1/D2=Dens, TR=Trap, ~~=Water | Number indicates player (1 or 2)")

    def get_user_input(self) -> str:
        """
        Get move input from the user.

        Returns:
            User input string (stripped of whitespace)
        """
        return input(
            "\nEnter your move (e.g., 'A1 to B2'), 'undo' to undo last move, or 'quit' to exit: "
        )

    def display_message(self, message: str) -> None:
        """
        Display a message to the user.

        Args:
            message: Message to display
        """
        print(message)
