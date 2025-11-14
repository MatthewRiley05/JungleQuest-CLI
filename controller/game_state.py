"""
Game State Manager Module

Handles game state management including undo functionality.
"""

from typing import Dict, List, Any
from model.piece import Piece
from model.board import Board


class GameStateManager:
    """Manages game state and undo functionality."""

    def __init__(self, max_undos: int = 3):
        """Initialize the game state manager."""
        self.move_history = []  # Stack to store move history for undo
        self.undo_count = 0  # Track number of undos used (max 3 per game)
        self.MAX_UNDOS = max_undos

    def _save_game_state(self, board: Board, current_turn: int):
        """Save the current game state before a move for potential undo."""
        # Create a deep copy of the board state
        board_state = {}
        for row in range(9):
            for col in range(7):
                tile = board.get_tile((col, row))
                piece = tile.get_piece()
                if piece:
                    # Store piece info: (name, owner, position)
                    board_state[(col, row)] = {"name": piece.name, "owner": piece.owner}

        # Save state with current player turn
        state = {"board": board_state, "current_turn": current_turn}
        self.move_history.append(state)

    def undo_move(self, board: Board, game):
        """Undo the last move if undos are available."""
        # Check if undos are available
        if self.undo_count >= self.MAX_UNDOS:
            print(f"Cannot undo: Maximum of {self.MAX_UNDOS} undos per game reached.")
            return False

        # Check if there's any move to undo
        if len(self.move_history) == 0:
            print("Cannot undo: No moves have been made yet.")
            return False

        # Restore the previous state
        previous_state = self.move_history.pop()

        # Clear the current board
        for row in range(9):
            for col in range(7):
                board.remove_piece((col, row))

        # Restore pieces to their previous positions
        for position, piece_info in previous_state["board"].items():
            # Recreate the piece
            piece = Piece(piece_info["name"], piece_info["owner"])
            board.place_piece(piece, position)

        # Restore the turn
        game.current_turn = previous_state["current_turn"]

        # Increment undo counter
        self.undo_count += 1

        print(f"✓ Move undone! ({self.MAX_UNDOS - self.undo_count} undos remaining)")
        return True

    def get_undos_remaining(self) -> int:
        """Get the number of undos remaining."""
        return self.MAX_UNDOS - self.undo_count