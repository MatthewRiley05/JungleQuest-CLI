"""
Move Validator Module

Handles all move validation logic for the JungleQuest game.
"""

from model.tile import Tile
from model.piece import Piece
from model.board import Board


class MoveValidator:
    """Validates moves according to game rules."""

    def __init__(self, board: Board):
        """Initialize with reference to game board."""
        self.board = board

    def is_valid_move(
        self,
        from_position: tuple[int, int],
        to_position: tuple[int, int],
        current_player: int,
    ) -> bool:
        """
        Validate if a move is legal according to game rules.

        Args:
            from_position: Starting position (col, row)
            to_position: Target position (col, row)
            current_player: Current player index (0 or 1)

        Returns:
            True if move is valid, False otherwise
        """
        piece: Piece = self.board.get_piece(from_position)

        # Lion/Tiger river jumping (3 cols horizontal or 4 rows vertical)
        if piece.name in ["Lion", "Tiger"]:
            from_col, from_row = from_position
            to_col, to_row = to_position
            if (
                from_row == to_row
                and abs(from_col - to_col) == 3
                and self._is_river_jump_clear(from_position, to_position, True)
            ):
                return True
            if (
                from_col == to_col
                and abs(from_row - to_row) == 4
                and self._is_river_jump_clear(from_position, to_position, False)
            ):
                return True

        # Check piece ownership
        if current_player != piece.owner:
            return False

        # Prevent moving into own den
        own_den = (
            self.board.PLAYER_1_DEN_POSITION
            if current_player == 0
            else self.board.PLAYER_2_DEN_POSITION
        )
        if to_position == own_den:
            return False

        # Only rats can enter water
        if (
            piece.name != "Rat"
            and self.board.get_tile(to_position).tile_type == Tile.WATER
        ):
            return False

        # Must move exactly one tile (orthogonal)
        return (
            abs(from_position[0] - to_position[0])
            + abs(from_position[1] - to_position[1])
            == 1
        )

    def _is_river_jump_clear(self, from_pos, to_pos, is_horizontal):
        """Check if river jump path is clear of rats."""
        if is_horizontal:
            col_range = range(
                min(from_pos[0], to_pos[0]) + 1, max(from_pos[0], to_pos[0])
            )
            return all(
                self.board.get_tile((col, from_pos[1])).tile_type == Tile.WATER
                and self.board.get_tile((col, from_pos[1])).is_empty()
                for col in col_range
            )
        else:
            row_range = range(
                min(from_pos[1], to_pos[1]) + 1, max(from_pos[1], to_pos[1])
            )
            return all(
                self.board.get_tile((from_pos[0], row)).tile_type == Tile.WATER
                and self.board.get_tile((from_pos[0], row)).is_empty()
                for row in row_range
            )
