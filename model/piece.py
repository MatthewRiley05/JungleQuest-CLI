from .tile import Tile


class Piece:
    """Represents a game piece with rank and capture logic"""

    # Piece ranks (higher can capture lower, except special cases)
    RANKS = {
        "Rat": 1,
        "Cat": 2,
        "Dog": 3,
        "Wolf": 4,
        "Leopard": 5,
        "Tiger": 6,
        "Lion": 7,
        "Elephant": 8,
    }

    # Player identifiers
    PLAYER_1 = 0
    PLAYER_2 = 1

    def __init__(self, name: str, owner: int):
        self.name = name
        self.rank = self.RANKS[name]
        self.owner = owner

    def __str__(self):
        return self.name[0]

    def can_capture(self, self_tile: Tile, opponent, opponent_tile: Tile) -> bool:
        """
        Determine if this piece can capture an opponent piece.
        Special rules:
        - Rat can capture Elephant (only on land)
        - Rat can capture Rat (only if both on same terrain type)
        - Elephant cannot capture Rat
        - Otherwise, higher/equal rank can capture lower rank
        """
        # Rat special cases
        if self.name == "Rat":
            if opponent.name == "Elephant":
                return self_tile.tile_type != Tile.WATER
            if opponent.name == "Rat":
                return self_tile.tile_type == opponent_tile.tile_type

        # Elephant cannot capture Rat
        if self.name == "Elephant" and opponent.name == "Rat":
            return False

        # Standard rank-based capture
        return self.rank >= opponent.rank
