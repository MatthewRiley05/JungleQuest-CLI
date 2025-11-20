"""
Move Parser Module

Handles parsing and validation of user input for moves.
"""

import re
from typing import Optional, Tuple


class MoveParser:
    """Parses and validates user move input."""

    @staticmethod
    def parse_move_input(
        input: str,
    ) -> Tuple[Optional[Tuple[int, int]], Optional[Tuple[int, int]]]:
        """
        Parse move input string into board coordinates.

        Args:
            input: User input like "A1 to B2"

        Returns:
            Tuple of (from_position, to_position) or (None, None) if invalid
        """
        pattern = r"^[A-Ga-g][1-9] to [A-Ga-g][1-9]$"  # valid characters include A-G, a-g, 1-9

        if not re.match(pattern, input):
            print(
                "Invalid input format. Please enter a valid move (e.g: A1 to A2, B4 to C4)"
            )
            return None, None  # means input is invalid.

        from_part, to_part = input.split(" to ")

        from_position = MoveParser.convert_to_coordinates(from_part)
        to_position = MoveParser.convert_to_coordinates(to_part)

        if not from_position or not to_position:
            print(
                "Input is out of bounds. Please enter a valid move (e.g: A1 to A2, B4 to C4)"
            )
            return None, None

        return from_position, to_position

    @staticmethod
    def convert_to_coordinates(position: str) -> Optional[Tuple[int, int]]:
        """
        Convert board notation (e.g., "A1") to coordinates.

        Args:
            position: Board position like "A1"

        Returns:
            Tuple of (column, row) or None if invalid
        """
        column = ord(position[0].upper()) - ord("A")
        row = int(position[1]) - 1
        return (column, row) if 0 <= column < 7 and 0 <= row < 9 else None
