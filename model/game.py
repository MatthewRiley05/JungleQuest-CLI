"""
Game Module

This module contains the Game class which manages the overall game state,
including players, the board, and turn management.
"""

from typing import List
from .board import Board
from .player import Player


class Game:
    """
    Manages the overall game state and flow.

    Attributes:
        board: The game board
        players: List of two Player objects
        current_turn: Index of current player (0 or 1)
    """

    def __init__(self, player1_name: str, player2_name: str) -> None:
        """
        Initialize a new game with two players.

        Args:
            player1_name: Name of the first player
            player2_name: Name of the second player
        """
        self.board = Board()
        self.players: List[Player] = [Player(player1_name), Player(player2_name)]
        self.current_turn = 0  # Player 1 starts

    def switch_turn(self) -> None:
        """Switch to the next player's turn."""
        self.current_turn = (self.current_turn + 1) % 2

    def display_status(self):
        self.board.display_board()
        print(f"Current turn: {self.players[self.current_turn].name}")
