from .piece import Piece

class Tile:
    LAND = 'L'
    PLAYER_1_DEN = 'D1'
    PLAYER_2_DEN = 'D2'
    TRAP = 'T'
    WATER = 'W'

    # possible owners
    PLAYER_1 = "P1"
    PLAYER_2 = "P2"
    NEUTRAL = ""

    def __init__(self, tile_type=LAND, piece : Piece = None, owner : str = NEUTRAL):
        self.tile_type = tile_type  # Type of the tile (land, den, trap, water)
        self.piece = piece  # Piece occupying the tile (empty. rat, cat, dog, .., elephant)
        self.owner = owner

    def is_empty(self):
        return self.piece is None

    
    def place_piece(self, piece : Piece):
        self.piece = piece

    def remove_piece(self):
        self.piece = None

    def __str__(self):
        piece_name_and_owner = "None."
        if self.is_empty() == False:
            piece_name_and_owner = self.piece.name + " (" + self.piece.owner + ")."
        return str(self.tile_type) + ", " + piece_name_and_owner 