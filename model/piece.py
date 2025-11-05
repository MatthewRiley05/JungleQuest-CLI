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

    def can_capture(self, opponent) -> bool:
        if self.name == 'Rat' and opponent.name == 'Elephant':
            return True
        if self.name == 'Elephant' and opponent.name == 'Rat':
            return False
        if self.rank < opponent.rank:
            return False
        return True