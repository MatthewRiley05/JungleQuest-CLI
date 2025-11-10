from model.game import Game
from model.board import Board
from model.tile import Tile
from model.piece import Piece
from view.view import View

import re


class Controller:
    def __init__(self):
        self.view = View()
        self.game = None

    def start_game(self):
        print("Starting game...")
        player1_name = input("Enter name for Player 1: ")
        player2_name = input("Enter name for Player 2: ")
        self.game = Game(player1_name, player2_name)
        self.play_game()

    def play_game(self):
        game_over = False
        while not game_over:
            self.view.display_board(self.game.board)
            self.view.display_turn(self.game.players[self.game.current_turn].name)

            move = self.view.get_user_input()
            if move.lower() == "quit":
                print("Terminating game session...")
                break

            # attempt to take a turn
            result = self.take_turn(move)
            if result is None:
                continue  # await new input from the user (invalid move)
            elif result is True:
                # Game won!
                game_over = True
            else:
                # Valid move but game continues
                self.game.switch_turn()

    def parse_move_input(self, input: str):
        pattern = r"^[A-Ga-g][1-9] to [A-Ga-g][1-9]$"  # valid characters include A-G, a-g, 1-9

        if not re.match(pattern, input):
            print(
                "Invalid input format. Please enter a valid move (e.g: A1 to A2, B4 to C4)"
            )
            return None, None  # means input is invalid.

        from_part, to_part = input.split(" to ")

        if not self.convert_to_coordinates(
            from_part
        ) or not self.convert_to_coordinates(to_part):
            print(
                "Input is out of bounds. Please enter a valid move (e.g: A1 to A2, B4 to C4)"
            )
            return None, None
        from_position = self.convert_to_coordinates(from_part)
        to_position = self.convert_to_coordinates(to_part)

        return from_position, to_position

    def is_valid_move(
        self, from_position: tuple[int, int], to_position: tuple[int, int]
    ) -> bool:
        row_difference = abs(from_position[0] - to_position[0])
        col_difference = abs(from_position[1] - to_position[1])

        # Check if the movement is only one tile upwards, downwards, left or right.
        if row_difference + col_difference != 1:
            return False

        piece: Piece = self.game.board.get_piece(from_position)
        # Check if the piece is owned by the current player.
        # note: current_turn = 0 if player 1's turn, 1 if player 2's turn.
        if self.game.current_turn != piece.owner:
            return False

        # Check if the move leads to the player's own den
        if (
            self.game.current_turn == 0
            and to_position == self.game.board.PLAYER_1_DEN_POSITION
        ):
            return False
        if (
            self.game.current_turn == 1
            and to_position == self.game.board.PLAYER_2_DEN_POSITION
        ):
            return False

        # Check if a non-rat piece tried to move into a water tile.
        if (
            piece.name != "Rat"
            and self.game.board.get_tile(to_position).tile_type == Tile.WATER
        ):
            return False

        return True

    def convert_to_coordinates(self, position):
        # Convert a position string like "A1" to a tuple (row, column)
        # column = ord(position[0].upper()) - ord('A')  # Convert 'A'-'G' to 0-6
        # row = int(position[1]) - 1  # Convert '1'-'9' to 0-8
        # return (row, column) if 0 <= row < 7 and 0 <= column < 9 else (None, None)
        column = -1
        match position[0].upper():
            case "A":
                column = 0
            case "B":
                column = 1
            case "C":
                column = 2
            case "D":
                column = 3
            case "E":
                column = 4
            case "F":
                column = 5
            case "G":
                column = 6
        row = int(position[1]) - 1
        return (column, row)

    def take_turn(self, move):
        # Validate the move string format
        from_position, to_position = self.parse_move_input(move)

        if not from_position or not to_position:
            return None  # for invalid inputs

        current_player = self.game.current_turn  # 0 for player 1, 1 for player 2
        piece_to_move: Piece = self.game.board.get_piece(from_position)

        if piece_to_move is None:
            print("Invalid move. A tile with no piece was selected. Please try again.")
            return None

        if not self.is_valid_move(from_position, to_position):
            print(
                "Invalid move. You may only move your own piece by one tile horizontally/vertically, and never into its own den or water (except rats)"
            )
            return None

        # Check if the target tile is occupied
        target_tile: Tile = self.game.board.get_tile(to_position)
        target_piece: Piece = target_tile.get_piece()

        if target_piece is not None:
            # Check if trying to capture own piece
            if target_piece.owner == current_player:
                print(
                    "Invalid move: You cannot move to a tile occupied by your own piece."
                )
                return None
            # Opponent's piece - check if capture is valid
            elif not piece_to_move.can_capture(
                self.game.board.get_tile(from_position), target_piece, target_tile
            ):
                print("Invalid move: Your piece cannot capture the opponent's piece.")
                return None
            # Valid capture - remove the opponent's piece
            print(
                f"{self.game.players[current_player].name} captured {target_piece.name}!"
            )
            self.game.board.remove_piece(to_position)

        # Move piece
        self.game.board.remove_piece(from_position)
        self.game.board.place_piece(piece_to_move, to_position)

        # Check for win conditions
        if self.check_win_condition(to_position):
            return True

        # Valid move, game continues
        return False

    def check_win_condition(self, to_position: tuple[int, int]) -> bool:
        """
        Check if the game has been won.
        Win conditions:
        1. A player moves into the opponent's den
        2. A player captures all opponent's pieces
        """
        current_player = self.game.current_turn

        # Win Condition 1: Player entered opponent's den
        if current_player == 0 and to_position == self.game.board.PLAYER_2_DEN_POSITION:
            self.view.display_board(self.game.board)
            print(
                f"\n🎉 {self.game.players[current_player].name} wins by entering the opponent's den! 🎉"
            )
            return True
        elif (
            current_player == 1 and to_position == self.game.board.PLAYER_1_DEN_POSITION
        ):
            self.view.display_board(self.game.board)
            print(
                f"\n🎉 {self.game.players[current_player].name} wins by entering the opponent's den! 🎉"
            )
            return True

        # Win Condition 2: Opponent has no pieces left
        opponent = 1 - current_player
        opponent_pieces_count = self.count_player_pieces(opponent)

        if opponent_pieces_count == 0:
            self.view.display_board(self.game.board)
            print(
                f"\n🎉 {self.game.players[current_player].name} wins by capturing all opponent pieces! 🎉"
            )
            return True

        return False

    def count_player_pieces(self, player: int) -> int:
        """Count the number of pieces a player has on the board."""
        count = 0
        for column in self.game.board.grid:
            for tile in column:
                piece = tile.get_piece()
                if piece is not None and piece.owner == player:
                    count += 1
        return count

    def end_turn(self):
        # Switch to the next player
        self.game.current_turn = (self.game.current_turn + 1) % len(self.game.players)
        print(f"Now is {self.game.players[self.game.current_turn].name}'s turn.")
