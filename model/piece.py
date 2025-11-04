class Piece:
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

    def __init__(self, name : str):
        self.name = name
        self.rank = self.RANKS[name]

    def __str__(self):
        return f"{self.name[0]}"

    def can_capture(self, opponent):
        if self.rank < opponent.rank:
            return False
        if self.name == 'Rat' and opponent.name == 'Elephant':
            return False
        return True