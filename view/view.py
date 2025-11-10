from model.board import Board


class View:
    # Display constants
    BOARD_WIDTH = 60
    HEADER_PADDING = 20
    COLUMN_WIDTH = 6
    COLUMNS = ["A", "B", "C", "D", "E", "F", "G"]

    # Piece abbreviations
    PIECE_ABBREV = {
        "Rat": "R",
        "Cat": "C",
        "Dog": "D",
        "Wolf": "W",
        "Leopard": "P",
        "Tiger": "T",
        "Lion": "L",
        "Elephant": "E",
    }

    # Tile symbols
    TILE_SYMBOLS = {
        "L": "  ",  # Land
        "D1": "D1",  # Player 1 Den
        "D2": "D2",  # Player 2 Den
        "T": "TR",  # Trap
        "W": "~~",  # Water
    }

    def display_board(self, board: Board):
        """Display the game board with pieces and special tiles"""
        print("\n" + "=" * self.BOARD_WIDTH)
        print(" " * self.HEADER_PADDING + "JUNGLE QUEST")
        print("=" * self.BOARD_WIDTH)

        # Column headers
        self._print_column_headers()
        print("   +" + "------+" * len(self.COLUMNS))

        # Display board rows
        for i in range(board.MAX_ROWS):
            print(f" {i + 1} |", end="")
            for j in range(board.MAX_COLUMNS):
                print(f"{self._format_tile(board.grid[j][i])}|", end="")
            print(f" {i + 1}")
            print("   +" + "------+" * len(self.COLUMNS))

        # Column headers at bottom
        self._print_column_headers()
        print("=" * self.BOARD_WIDTH)

    def _print_column_headers(self):
        """Print column headers (A-G)"""
        print("    ", end="")
        for col in self.COLUMNS:
            print(f" {col:^{self.COLUMN_WIDTH}}", end="")
        print()

    def _format_tile(self, tile):
        """Format a tile for display with piece and tile type info"""
        if not tile.is_empty():
            piece = tile.piece
            piece_abbr = self.PIECE_ABBREV.get(piece.name, piece.name[0])
            return f"{piece_abbr}{piece.owner + 1:^{self.COLUMN_WIDTH - 1}}"

        tile_display = self.TILE_SYMBOLS.get(tile.tile_type, tile.tile_type)
        return f"{tile_display:^{self.COLUMN_WIDTH}}"

    def display_turn(self, player_name):
        print(f"\n>>> Current turn: {player_name}")
        print(
            "Pieces: R=Rat, C=Cat, D=Dog, W=Wolf, P=Leopard, T=Tiger, L=Lion, E=Elephant"
        )
        print("Tiles: D1/D2=Dens, TR=Trap, ~~=Water | Number indicates player (1 or 2)")

    def get_user_input(self):
        return input("\nEnter your move (e.g., 'A1 to B2') or 'quit' to exit: ")

    def display_message(self, message):
        print(message)
