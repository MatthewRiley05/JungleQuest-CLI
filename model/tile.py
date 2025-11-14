"""
Tile Module

This module contains the Tile class representing a single board tile.
"""


class Tile:
    """
    Represents a single tile on the game board.

    Each tile has a type (land, water, den, trap) and may contain a piece.

    Attributes:
        LAND: Constant for land tile type
        PLAYER_1_DEN: Constant for Player 1's den
        PLAYER_2_DEN: Constant for Player 2's den
        TRAP: Constant for trap tile type
        WATER: Constant for water tile type
        PLAYER_1: Constant for Player 1 ownership
        PLAYER_2: Constant for Player 2 ownership
        NEUTRAL: Constant for neutral tiles
        tile_type: Type of this tile
        piece: Piece occupying this tile (None if empty)
        owner: Player who owns this tile (for traps)
    """

    # Tile types
    LAND = "L"
    PLAYER_1_DEN = "D1"
    PLAYER_2_DEN = "D2"
    TRAP = "T"
    WATER = "W"

    # Tile ownership
    PLAYER_1 = 0
    PLAYER_2 = 1
    NEUTRAL = -1

    def __init__(self, tile_type: str = LAND, piece=None, owner: str = -1) -> None:
        """
        Initialize a tile.

        Args:
            tile_type: Type of tile (default: LAND)
            piece: Piece on this tile (default: None)
            owner: Owner of this tile for traps (default: NEUTRAL)
        """
        self.tile_type = tile_type  # Type of the tile (land, den, trap, water)
        self.piece = (
            piece  # Piece occupying the tile (empty. rat, cat, dog, .., elephant)
        )
        self.owner = owner

    def is_empty(self) -> bool:
        """
        Check if the tile is empty.

        Returns:
            True if no piece occupies this tile, False otherwise
        """
        return self.piece is None

    def get_piece(self):
        """
        Get the piece on this tile.

        Returns:
            The Piece on this tile, or None if empty
        """
        return self.piece

    def place_piece(self, piece) -> None:
        """
        Place a piece on this tile.

        Args:
            piece: The piece to place
        """
        self.piece = piece

    # def remove_piece(self):
    #     self.piece = None

    def __str__(self):
        piece_name_and_owner = ""
        padding = ""

        if not self.is_empty():
            piece_name_and_owner = (
                ", " + self.piece.name + "(P" + str(self.piece.owner + 1) + ")"
            )

        for i in range(12 - len(piece_name_and_owner)):
            padding += " "
        return str(self.tile_type) + piece_name_and_owner + padding + "|"
