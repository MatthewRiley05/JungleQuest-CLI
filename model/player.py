"""
Player Module

This module contains the Player class representing a game player.
"""

from typing import List


class Player:
    """
    Represents a player in the game.

    Attributes:
        name: The player's name
        pieces: List of pieces owned by this player (currently unused)
    """

    def __init__(self, name: str) -> None:
        """
        Initialize a player.

        Args:
            name: The player's name
        """
        self.name = name
        self.pieces: List = []

    def add_piece(self, piece):
        self.pieces.append(piece)

    def get_pieces(self):
        return self.pieces
