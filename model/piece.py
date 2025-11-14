"""
Piece Module

This module contains the Piece class representing game pieces
and their capture rules.
"""

from typing import Dict
from .tile import Tile


class Piece:
    """
    Represents a game piece with rank and capture rules.

    Each piece has a name, rank, and owner. Pieces can capture
    other pieces based on rank and special rules.

    Attributes:
        RANKS: Dictionary mapping piece names to their ranks
        PLAYER_1: Constant for player 1 (0)
        PLAYER_2: Constant for player 2 (1)
        name: Name of the piece (e.g., "Rat", "Elephant")
        rank: Numeric rank of the piece (1-8)
        owner: Player who owns this piece (0 or 1)
    """

    # pieces can capture other pieces of the same or lower ranks
    # the rat may capture the elephant.
    # the elephant may not capture the rat.
    RANKS: Dict[str, int] = {
        "Rat": 1,
        "Cat": 2,
        "Dog": 3,
        "Wolf": 4,
        "Leopard": 5,
        "Tiger": 6,
        "Lion": 7,
        "Elephant": 8,
    }

    # possible owners
    PLAYER_1 = 0
    PLAYER_2 = 1

    def __init__(self, name: str, owner) -> None:
        """
        Initialize a piece.

        Args:
            name: Name of the piece (must be in RANKS)
            owner: Player who owns this piece (0 or 1)
        """
        self.name = name
        self.rank = self.RANKS[name]
        self.owner = owner

    def __str__(self):
        return f"{self.name[0]}"

    def can_capture(self, self_tile: Tile, opponent, opponent_tile: Tile) -> bool:
        # Trap rule: If your opponent is in your trap, you can capture it
        if opponent_tile.tile_type == Tile.TRAP and opponent_tile.owner == self.owner:
            return True

        if self.name == "Rat":
            # Rat in water cannot capture pieces on land (and vice versa)
            if (
                self_tile.tile_type == Tile.WATER
                and opponent_tile.tile_type != Tile.WATER
            ):
                return False
            if (
                self_tile.tile_type != Tile.WATER
                and opponent_tile.tile_type == Tile.WATER
            ):
                return False

            # Rat can capture Elephant only if both are on land
            if (
                opponent.name == "Elephant"
                and self_tile.tile_type != Tile.WATER
                and opponent_tile.tile_type != Tile.WATER
            ):
                return True

            # Rat vs Rat: can only capture if in same environment (both water or both land)
            if opponent.name == "Rat" and (
                (
                    self_tile.tile_type == Tile.LAND
                    and opponent_tile.tile_type == Tile.LAND
                )
                or (
                    self_tile.tile_type == Tile.WATER
                    and opponent_tile.tile_type == Tile.WATER
                )
            ):
                return True

        if self.name == "Elephant" and opponent.name == "Rat":
            return False

        if self.rank >= opponent.rank:
            return True

        return False
