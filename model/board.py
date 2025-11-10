from .tile import Tile
from .piece import Piece


class Board:
    MAX_COLUMNS = 7
    MAX_ROWS = 9

    PLAYER_1_DEN_POSITION: tuple[int, int] = (3, 0)
    PLAYER_2_DEN_POSITION: tuple[int, int] = (3, 8)

    # BOARD
    # # A B C D E F G
    # 1
    # 2
    # 3
    # 4
    # 5
    # 6
    # 7
    # 8
    # 9

    def __init__(self):
        self.grid = self.initialize_empty_board()
        self.initialize_special_tiles()
        self.initialize_pieces()

    def initialize_empty_board(self):
        # Fill the board with empty, land (default) tiles.
        # The double list is filled with 7 lists, each containing 9 elements.
        # Each inner list represents a column from top to bottom.
        return [[Tile() for _ in range(self.MAX_ROWS)] for _ in range(self.MAX_COLUMNS)]

    def initialize_special_tiles(self):
        # Dens
        self.grid[3][0] = Tile(Tile.PLAYER_1_DEN, None)
        self.grid[3][8] = Tile(Tile.PLAYER_2_DEN, None)

        # Traps (3 surrounding each den)
        for col in [2, 3, 4]:
            row = 0 if col != 3 else 1
            self.grid[col][row] = Tile(Tile.TRAP, None, Tile.PLAYER_1)
            row = 8 if col != 3 else 7
            self.grid[col][row] = Tile(Tile.TRAP, None, Tile.PLAYER_2)

        # Rivers (two 2x3 sections)
        for col in [1, 2, 4, 5]:
            for row in [3, 4, 5]:
                self.grid[col][row] = Tile(Tile.WATER, None)

    def initialize_pieces(self):
        # Piece positions: (name, col_p1, row_p1, col_p2, row_p2)
        pieces = [
            ("Elephant", 6, 2, 0, 6), ("Tiger", 6, 0, 0, 8), ("Cat", 5, 1, 1, 7),
            ("Wolf", 4, 2, 2, 6), ("Leopard", 2, 2, 4, 6), ("Dog", 1, 1, 5, 7),
            ("Rat", 0, 2, 6, 6), ("Lion", 0, 0, 6, 8)
        ]
        for name, c1, r1, c2, r2 in pieces:
            self.place_piece(Piece(name, Piece.PLAYER_1), (c1, r1))
            self.place_piece(Piece(name, Piece.PLAYER_2), (c2, r2))

    def place_piece(self, piece: Piece, position: tuple[int, int]):
        x, y = position
        tile: Tile = self.grid[x][y]
        if tile.is_empty():
            tile.place_piece(piece)
        else:
            print("Cannot place piece here.")

    def remove_piece(self, position: tuple[int, int]):
        x, y = position
        tile: Tile = self.grid[x][y]
        tile.piece = None

    def get_piece(self, position):
        x, y = position
        return self.grid[x][y].piece

    def get_tile(self, position):
        x, y = position
        return self.grid[x][y]
