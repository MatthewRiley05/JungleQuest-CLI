from .tile import Tile
class Piece:
    # pieces can capture other pieces of the same or lower ranks
    # the rat may capture the elephant.
    # the elephant may not capture the rat.
    RANKS = {
        'Rat': 1,
        'Cat': 2,
        'Dog': 3,
        'Wolf': 4,
        'Leopard': 5,
        'Tiger': 6,
        'Lion': 7,
        'Elephant': 8
    }

    # possible owners
    PLAYER_1 = "P1"
    PLAYER_2 = "P2"


    def __init__(self, name : str, owner : str):
        self.name = name
        self.rank = self.RANKS[name]
        self.owner = owner

    def __str__(self):
        return f"{self.name[0]}"

    def can_capture(self, self_tile : Tile, opponent, opponent_tile : Tile) -> bool:
        if self.name == 'Rat':
            if opponent.name == 'Elephant' and self_tile.tile_type != Tile.WATER:
                return True
            if opponent.name == 'Rat' and ((self_tile.tile_type == Tile.LAND and opponent_tile.tile_type == Tile.LAND) or (self_tile.tile_type == Tile.WATER and opponent_tile.tile_type == Tile.WATER)):
                return True

        if self.name == 'Elephant' and opponent.name == 'Rat':
            return False
        
        if self.rank >= opponent.rank:
            return True
         
        return False