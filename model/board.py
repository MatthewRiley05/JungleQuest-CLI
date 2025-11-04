from tile import Tile
from piece import Piece

class Board:
    def __init__(self):
        self.grid = self.initialize_empty_board()
        self.initialize_special_tiles()
        self.initialize_pieces()

    def initialize_empty_board(self):
        # Fill the board with empty, land (default) tiles.
        return [[Tile() for _ in range(9)] for _ in range(7)]

    def initialize_special_tiles(self):
        self.grid[3][0] = Tile(Tile.DEN) # northern den 
        self.grid[3][8] = Tile(Tile.DEN) # southern den
        
        # northern den traps
        self.grid[2][0] = Tile(Tile.TRAP, None) 
        self.grid[3][1] = Tile(Tile.TRAP, None) 
        self.grid[3][1] = Tile(Tile.TRAP, None) 
        # southern den traps
        self.grid[3][7] = Tile(Tile.TRAP, None)  
        self.grid[2][8] = Tile(Tile.TRAP, None) 
        self.grid[4][8] = Tile(Tile.TRAP, None) 

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
        # southern pieces
        self.place_piece(Piece('Elephant'), (0, 6))
        self.place_piece(Piece('Tiger'), (0, 8))
        self.place_piece(Piece('Cat'), (1, 7))
        self.place_piece(Piece('Wolf'), (2, 6))
        self.place_piece(Piece('Leopard'), (4, 6))
        self.place_piece(Piece('Dog'), (5, 7))
        self.place_piece(Piece('Rat'), (6, 6))
        self.place_piece(Piece('Lion'), (6, 8))

        # northern pieces
        self.place_piece(Piece('Elephant'), (6, 2))
        self.place_piece(Piece('Tiger'), (6, 0))
        self.place_piece(Piece('Cat'), (5, 1))
        self.place_piece(Piece('Wolf'), (4, 2))
        self.place_piece(Piece('Leopard'), (2, 2))
        self.place_piece(Piece('Dog'), (1, 1))
        self.place_piece(Piece('Rat'), (0, 2))
        self.place_piece(Piece('Lion'), (0, 0))
        
        

    def place_piece(self, piece: Piece, position: tuple[int, int]):
        x, y = position
        tile : Tile = self.grid[x][y]
        if tile.is_empty():
            if tile.tile_type == Tile.LAND:  # Pieces can only occupy land tiles
                tile.place_piece(piece)
            # WIP: rat special rules, etc

        else:
            print("You cannot place this piece on this tile.")

    def get_piece(self, position):
        x, y = position
        return self.grid[x][y].piece

    def display_board(self):
        for row in self.grid:
            print(' '.join([str(tile) for tile in row]))