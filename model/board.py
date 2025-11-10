from .tile import Tile
from .piece import Piece


class Board:
    MAX_COLUMNS = 7
    MAX_ROWS = 9

    PLAYER_1_DEN_POSITION: tuple[int, int] = (3, 0)
    PLAYER_2_DEN_POSITION: tuple[int, int] = (3, 8)

    # Special tile positions as class constants
    PLAYER_1_TRAPS = [(2, 0), (3, 1), (4, 0)]
    PLAYER_2_TRAPS = [(3, 7), (2, 8), (4, 8)]
    LEFT_RIVER = [(1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5)]
    RIGHT_RIVER = [(4, 3), (4, 4), (4, 5), (5, 3), (5, 4), (5, 5)]

    # Initial piece positions
    PLAYER_1_PIECES = [
        ("Lion", (0, 0)),
        ("Dog", (1, 1)),
        ("Rat", (0, 2)),
        ("Leopard", (2, 2)),
        ("Wolf", (4, 2)),
        ("Cat", (5, 1)),
        ("Tiger", (6, 0)),
        ("Elephant", (6, 2)),
    ]
    PLAYER_2_PIECES = [
        ("Elephant", (0, 6)),
        ("Cat", (1, 7)),
        ("Wolf", (2, 6)),
        ("Leopard", (4, 6)),
        ("Dog", (5, 7)),
        ("Rat", (6, 6)),
        ("Tiger", (0, 8)),
        ("Lion", (6, 8)),
    ]

    def __init__(self):
        self.grid = self.initialize_empty_board()
        self.initialize_special_tiles()
        self.initialize_pieces()

    def initialize_empty_board(self):
        """Fill board with empty land tiles"""
        return [[Tile() for _ in range(self.MAX_ROWS)] for _ in range(self.MAX_COLUMNS)]

    def initialize_special_tiles(self):
        """Initialize dens, traps, and water tiles"""
        # Dens
        self.grid[self.PLAYER_1_DEN_POSITION[0]][self.PLAYER_1_DEN_POSITION[1]] = Tile(
            Tile.PLAYER_1_DEN, None
        )
        self.grid[self.PLAYER_2_DEN_POSITION[0]][self.PLAYER_2_DEN_POSITION[1]] = Tile(
            Tile.PLAYER_2_DEN, None
        )

        # Player 1 traps
        for x, y in self.PLAYER_1_TRAPS:
            self.grid[x][y] = Tile(Tile.TRAP, None, Tile.PLAYER_1)

        # Player 2 traps
        for x, y in self.PLAYER_2_TRAPS:
            self.grid[x][y] = Tile(Tile.TRAP, None, Tile.PLAYER_2)

        # Rivers (water tiles)
        for x, y in self.LEFT_RIVER + self.RIGHT_RIVER:
            self.grid[x][y] = Tile(Tile.WATER, None)

    def initialize_pieces(self):
        """Place all pieces in their starting positions"""
        # Player 1 pieces
        for name, position in self.PLAYER_1_PIECES:
            self.place_piece(Piece(name, Piece.PLAYER_1), position)

        # Player 2 pieces
        for name, position in self.PLAYER_2_PIECES:
            self.place_piece(Piece(name, Piece.PLAYER_2), position)

    def place_piece(self, piece: Piece, position: tuple[int, int]):
        """Place a piece at the specified position if valid"""
        x, y = position
        tile: Tile = self.grid[x][y]

        if tile.is_empty() and (
            tile.tile_type == Tile.LAND
            or (tile.tile_type == Tile.WATER and piece.name == "Rat")
        ):
            tile.place_piece(piece)

    def remove_piece(self, position: tuple[int, int]):
        """Remove piece from the specified position"""
        x, y = position
        self.grid[x][y].piece = None

    def get_piece(self, position: tuple[int, int]):
        """Get piece at the specified position"""
        x, y = position
        return self.grid[x][y].piece

    def get_tile(self, position: tuple[int, int]):
        """Get tile at the specified position"""
        x, y = position
        return self.grid[x][y]
