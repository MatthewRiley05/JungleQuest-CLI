from model.board import Board


class View:
    def display_board(self, board: Board):
        print("\n" + "=" * 60)
        print(" " * 20 + "JUNGLE QUEST")
        print("=" * 60)

        # Column headers
        print("    ", end="")
        for col in ["A", "B", "C", "D", "E", "F", "G"]:
            print(f" {col:^6}", end="")
        print()
        print("   +" + "------+" * 7)

        # Display board from row 1 to row 9 (top to bottom)
        for i in range(board.MAX_ROWS):
            # Row number
            print(f" {i + 1} |", end="")

            # Display tiles in the row
            for j in range(board.MAX_COLUMNS):
                tile = board.grid[j][i]
                tile_str = self._format_tile(tile)
                print(f"{tile_str}|", end="")

            # Row number on the right side
            print(f" {i + 1}")
            print("   +" + "------+" * 7)

        # Column headers at bottom
        print("    ", end="")
        for col in ["A", "B", "C", "D", "E", "F", "G"]:
            print(f" {col:^6}", end="")
        print("\n" + "=" * 60)

    def _format_tile(self, tile):
        """Format a tile for display with piece and tile type info"""
        # Piece name abbreviations (to distinguish Lion from Leopard)
        piece_abbrev = {
            "Rat": "rat",
            "Cat": "cat",
            "Dog": "dog",
            "Wolf": "wlf",
            "Leopard": "lpd",  # P for Leopard
            "Tiger": "tgr",
            "Lion": "lio",
            "Elephant": "elp",
        }

        # Tile type symbols
        tile_symbols = {
            "L": "  ",  # Land (blank)
            "D1": "D1",  # Player 1 Den
            "D2": "D2",  # Player 2 Den
            "T": "TR",  # Trap
            "W": "~~",  # Water
        }

        if not tile.is_empty():
            piece = tile.piece
            # Use abbreviation + player number
            piece_abbr = piece_abbrev.get(piece.name, piece.name[0])
            piece_str = f"{piece_abbr}{piece.owner + 1}"
            # Show piece on any tile type
            return f"{piece_str:^6}"
        else:
            tile_display = tile_symbols.get(tile.tile_type, tile.tile_type)
            return f"{tile_display:^6}"

    def display_turn(self, player_name):
        print(f"\n>>> Current turn: {player_name}")
        print(
            "Pieces: R=rat, C=cat, D=dog, W=wlf, P=lpd, T=tgr, L=lio, E=elp"
        )
        print("Tiles: D1/D2=Dens, TR=Trap, ~~=Water | Number indicates player (1 or 2)")

    def get_user_input(self):
        return input("\nEnter your move (e.g., 'A1 to B2') or 'quit' to exit: ")

    def display_message(self, message):
        print(message)
