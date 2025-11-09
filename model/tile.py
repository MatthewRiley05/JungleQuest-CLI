class Tile:
    LAND = "L"
    PLAYER_1_DEN = "D1"
    PLAYER_2_DEN = "D2"
    TRAP = "T"
    WATER = "W"

    PLAYER_1 = 0
    PLAYER_2 = 1
    NEUTRAL = -1

    def __init__(self, tile_type=LAND, piece=None, owner: str = -1):
        self.tile_type = tile_type  # Type of the tile (land, den, trap, water)
        self.piece = (
            piece  # Piece occupying the tile (empty. rat, cat, dog, .., elephant)
        )
        self.owner = owner

    def is_empty(self):
        return self.piece is None

    def get_piece(self):
        return self.piece

    def place_piece(
        self,
        piece,
    ):
        self.piece = piece

    # def remove_piece(self):
    #     self.piece = None

    def __str__(self):
        piece_name_and_owner = ""
        padding = ""

        if not self.is_empty():
            piece_name_and_owner = (
                ", " + self.piece.name + "(P" + str(self.piece.owner + 1) + ")"
            )

        for i in range(12 - len(piece_name_and_owner)):
            padding += " "
        return str(self.tile_type) + piece_name_and_owner + padding + "|"
