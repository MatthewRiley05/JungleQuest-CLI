from piece import Piece
class Tile:
    LAND = 'L'
    DEN = 'D'
    TRAP = 'T'
    WATER = 'W'

    def __init__(self, tile_type=LAND, piece : Piece =None):
        self.tile_type = tile_type  # Type of the tile (land, den, trap, water)
        self.piece = piece  # Piece occupying the tile (empty. rat, cat, dog, .., elephant)

    def is_empty(self):
        return self.piece is None

    def place_piece(self, piece):
        self.piece = piece

    def remove_piece(self):
        self.piece = None

    def __str__(self):
        return str(self.tile_type + ", " + self.piece)