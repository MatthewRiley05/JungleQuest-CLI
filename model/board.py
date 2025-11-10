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
        # player 1 den
        self.grid[self.PLAYER_1_DEN_POSITION[0]][self.PLAYER_1_DEN_POSITION[1]] = Tile(
            Tile.PLAYER_1_DEN, None
        )
        # player 2 den
        self.grid[self.PLAYER_2_DEN_POSITION[0]][self.PLAYER_2_DEN_POSITION[1]] = Tile(
            Tile.PLAYER_2_DEN, None
        )

        # player 1 traps
        self.grid[2][0] = Tile(Tile.TRAP, None, Tile.PLAYER_1)
        self.grid[3][1] = Tile(Tile.TRAP, None, Tile.PLAYER_1)
        self.grid[4][0] = Tile(Tile.TRAP, None, Tile.PLAYER_1)
        # player 2 traps
        self.grid[3][7] = Tile(Tile.TRAP, None, Tile.PLAYER_2)
        self.grid[2][8] = Tile(Tile.TRAP, None, Tile.PLAYER_2)
        self.grid[4][8] = Tile(Tile.TRAP, None, Tile.PLAYER_2)

        # left river
        self.grid[1][3] = Tile(Tile.WATER, None)
        self.grid[1][4] = Tile(Tile.WATER, None)
        self.grid[1][5] = Tile(Tile.WATER, None)
        self.grid[2][3] = Tile(Tile.WATER, None)
        self.grid[2][4] = Tile(Tile.WATER, None)
        self.grid[2][5] = Tile(Tile.WATER, None)

        # right river
        self.grid[4][3] = Tile(Tile.WATER, None)
        self.grid[4][4] = Tile(Tile.WATER, None)
        self.grid[4][5] = Tile(Tile.WATER, None)
        self.grid[5][3] = Tile(Tile.WATER, None)
        self.grid[5][4] = Tile(Tile.WATER, None)
        self.grid[5][5] = Tile(Tile.WATER, None)

    def initialize_pieces(self):
        # player 1 pieces
        self.place_piece(Piece("Elephant", Piece.PLAYER_1), (6, 2))
        self.place_piece(Piece("Tiger", Piece.PLAYER_1), (6, 0))
        self.place_piece(Piece("Cat", Piece.PLAYER_1), (5, 1))
        self.place_piece(Piece("Wolf", Piece.PLAYER_1), (4, 2))
        self.place_piece(Piece("Leopard", Piece.PLAYER_1), (2, 2))
        self.place_piece(Piece("Dog", Piece.PLAYER_1), (1, 1))
        self.place_piece(Piece("Rat", Piece.PLAYER_1), (0, 2))
        self.place_piece(Piece("Lion", Piece.PLAYER_1), (0, 0))

        # player 2 pieces
        self.place_piece(Piece("Elephant", Piece.PLAYER_2), (0, 6))
        self.place_piece(Piece("Tiger", Piece.PLAYER_2), (0, 8))
        self.place_piece(Piece("Cat", Piece.PLAYER_2), (1, 7))
        self.place_piece(Piece("Wolf", Piece.PLAYER_2), (2, 6))
        self.place_piece(Piece("Leopard", Piece.PLAYER_2), (4, 6))
        self.place_piece(Piece("Dog", Piece.PLAYER_2), (5, 7))
        self.place_piece(Piece("Rat", Piece.PLAYER_2), (6, 6))
        self.place_piece(Piece("Lion", Piece.PLAYER_2), (6, 8))

    def place_piece(self, piece: Piece, position: tuple[int, int]):
        x, y = position
        tile: Tile = self.grid[x][y]
        if tile.is_empty():
            if tile.tile_type == Tile.LAND or (
                tile.tile_type == Tile.WATER and piece.name == "Rat"
            ):  # Pieces can only occupy land tiles
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
