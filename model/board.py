"""
Board Module

This module contains the Board class which represents the game board,
manages tiles, and handles piece placement and removal.
"""

from typing import Optional, Tuple
from .tile import Tile
from .piece import Piece


class Board:
    """
    Represents the JungleQuest game board.

    The board is a 7x9 grid containing different types of tiles
    (land, water, dens, traps) and manages piece placement.

    Attributes:
        MAX_COLUMNS: Number of columns (7, labeled A-G)
        MAX_ROWS: Number of rows (9, labeled 1-9)
        PLAYER_1_DEN_POSITION: Position of Player 1's den (D1)
        PLAYER_2_DEN_POSITION: Position of Player 2's den (D9)
        grid: 2D list of Tile objects representing the board
    """

    MAX_COLUMNS = 7
    MAX_ROWS = 9

    PLAYER_1_DEN_POSITION: Tuple[int, int] = (3, 0)
    PLAYER_2_DEN_POSITION: Tuple[int, int] = (3, 8)

    def __init__(self) -> None:
        """Initialize the board with tiles and pieces in starting positions."""
        self.grid = self.initialize_empty_board()
        self.initialize_special_tiles()
        self.initialize_pieces()

    def initialize_empty_board(self) -> list:
        """
        Create an empty board filled with default land tiles.

        Returns:
            2D list of Tile objects (columns x rows)
        """
        # Fill the board with empty, land (default) tiles.
        # The double list is filled with 7 lists, each containing 9 elements.
        # Each inner list represents a column from top to bottom.
        return [[Tile() for _ in range(self.MAX_ROWS)] for _ in range(self.MAX_COLUMNS)]

    def initialize_special_tiles(self) -> None:
        """
        Initialize special tiles (dens, traps, water) on the board.

        Layout:
        - Dens: D1 (Player 1) and D9 (Player 2)
        - Traps: 3 surrounding each den
        - Water: Two 2x3 river sections in the middle
        """
        # Dens
        self.grid[3][0] = Tile(Tile.PLAYER_1_DEN, None)
        self.grid[3][8] = Tile(Tile.PLAYER_2_DEN, None)

        # Traps (3 surrounding each den)
        for col in [2, 3, 4]:
            row = 0 if col != 3 else 1
            self.grid[col][row] = Tile(Tile.TRAP, None, Tile.PLAYER_1)
            row = 8 if col != 3 else 7
            self.grid[col][row] = Tile(Tile.TRAP, None, Tile.PLAYER_2)

        # Rivers (two 2x3 sections)
        for col in [1, 2, 4, 5]:
            for row in [3, 4, 5]:
                self.grid[col][row] = Tile(Tile.WATER, None)

    def initialize_pieces(self) -> None:
        """
        Place all pieces in their starting positions.

        Each player starts with 8 pieces:
        Elephant, Tiger, Cat, Wolf, Leopard, Dog, Rat, Lion
        """
        # Format: (name, col_p1, row_p1, col_p2, row_p2)
        piece_positions = [
            ("Elephant", 6, 2, 0, 6),
            ("Tiger", 6, 0, 0, 8),
            ("Cat", 5, 1, 1, 7),
            ("Wolf", 4, 2, 2, 6),
            ("Leopard", 2, 2, 4, 6),
            ("Dog", 1, 1, 5, 7),
            ("Rat", 0, 2, 6, 6),
            ("Lion", 0, 0, 6, 8),
        ]

        for name, col_p1, row_p1, col_p2, row_p2 in piece_positions:
            self.place_piece(Piece(name, Piece.PLAYER_1), (col_p1, row_p1))
            self.place_piece(Piece(name, Piece.PLAYER_2), (col_p2, row_p2))

    def place_piece(self, piece: Piece, position: Tuple[int, int]) -> bool:
        """
        Place a piece on the board at the specified position.

        Args:
            piece: The Piece object to place
            position: Target position as (col, row)

        Returns:
            True if piece placed successfully, False if position occupied
        """
        col, row = position
        tile: Tile = self.grid[col][row]
        if tile.is_empty():
            tile.place_piece(piece)
        else:
            print("Cannot place piece here.")

    def remove_piece(self, position: Tuple[int, int]) -> None:
        """
        Remove a piece from the board at the specified position.

        Args:
            position: Position to clear as (col, row)
        """
        col, row = position
        tile: Tile = self.grid[col][row]
        tile.piece = None

    def get_piece(self, position: Tuple[int, int]) -> Optional[Piece]:
        """
        Get the piece at the specified position.

        Args:
            position: Position to check as (col, row)

        Returns:
            The Piece at the position, or None if empty
        """
        col, row = position
        return self.grid[col][row].piece

    def get_tile(self, position: Tuple[int, int]) -> Tile:
        """
        Get the tile at the specified position.

        Args:
            position: Position to check as (col, row)

        Returns:
            The Tile at the position
        """
        col, row = position
        return self.grid[col][row]
