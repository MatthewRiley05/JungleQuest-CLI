class Tile:
    # Tile types
    LAND = "L"
    PLAYER_1_DEN = "D1"
    PLAYER_2_DEN = "D2"
    TRAP = "T"
    WATER = "W"

    # Tile owners
    PLAYER_1 = 0
    PLAYER_2 = 1
    NEUTRAL = -1

    def __init__(self, tile_type=LAND, piece=None, owner: int = NEUTRAL):
        self.tile_type = tile_type
        self.piece = piece
        self.owner = owner

    def is_empty(self):
        """Check if tile has no piece"""
        return self.piece is None

    def get_piece(self):
        """Get the piece on this tile"""
        return self.piece

    def place_piece(self, piece):
        """Place a piece on this tile"""
        self.piece = piece
