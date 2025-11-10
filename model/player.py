class Player:
    """Represents a player in the game"""

    def __init__(self, name: str):
        self.name = name
        self.pieces = []

    def add_piece(self, piece):
        """Add a piece to this player's collection"""
        self.pieces.append(piece)

    def get_pieces(self):
        """Get all pieces owned by this player"""
        return self.pieces
