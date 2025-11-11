from model.board import Board


class View:
    PIECE_ABBREV = {
        "Rat": "rat",
        "Cat": "cat",
        "Dog": "dog",
        "Wolf": "wlf",
        "Leopard": "lpd",
        "Tiger": "tgr",
        "Lion": "lio",
        "Elephant": "elp",
    }
    TILE_SYMBOLS = {"L": "  ", "D1": "D1", "D2": "D2", "T": "TR", "W": "~~"}

    def display_board(self, board: Board):
        print("\n" + "=" * 60)
        print(" " * 20 + "JUNGLE QUEST")
        print("=" * 60)

        self._print_column_headers()
        print("   +" + "------+" * 7)

        for i in range(board.MAX_ROWS):
            print(f" {i + 1} |", end="")
            for j in range(board.MAX_COLUMNS):
                print(f"{self._format_tile(board.grid[j][i])}|", end="")
            print(f" {i + 1}")
            print("   +" + "------+" * 7)

        self._print_column_headers()
        print("\n" + "=" * 60)

    def _print_column_headers(self):
        print("    ", end="")
        for col in "ABCDEFG":
            print(f" {col:^6}", end="")
        print()

    def _format_tile(self, tile):
        if not tile.is_empty():
            piece = tile.piece
            abbr = self.PIECE_ABBREV.get(piece.name, piece.name[0])
            piece_str = f"{abbr}{piece.owner + 1}"
            return f"{piece_str:^6}"
        return f"{self.TILE_SYMBOLS.get(tile.tile_type, tile.tile_type):^6}"

    def display_turn(self, player_name):
        print(f"\n>>> Current turn: {player_name}")
        print("Pieces: R=rat, C=cat, D=dog, W=wlf, P=lpd, T=tgr, L=lio, E=elp")
        print("Tiles: D1/D2=Dens, TR=Trap, ~~=Water | Number indicates player (1 or 2)")

    def get_user_input(self):
        return input(
            "\nEnter your move (e.g., 'A1 to B2'), 'undo' to undo last move, or 'quit' to exit: "
        )

    def display_message(self, message):
        print(message)
