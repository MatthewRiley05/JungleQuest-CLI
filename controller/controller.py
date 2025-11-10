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
        """Parse and validate move input format"""
        pattern = r"^[A-Ga-g][1-9] to [A-Ga-g][1-9]$"

        if not re.match(pattern, input):
            print(
                "Invalid input format. Please enter a valid move (e.g: A1 to A2, B4 to C4)"
            )
            return None, None

        from_part, to_part = input.split(" to ")
        from_position = self.convert_to_coordinates(from_part)
        to_position = self.convert_to_coordinates(to_part)

        if not from_position or not to_position:
            print(
                "Input is out of bounds. Please enter a valid move (e.g: A1 to A2, B4 to C4)"
            )
            return None, None

        return from_position, to_position

    def is_valid_move(
        self, from_position: tuple[int, int], to_position: tuple[int, int]
    ) -> bool:
        """Validate if a move is legal according to game rules"""
        # Check if movement is only one tile (horizontal or vertical)
        if (
            abs(from_position[0] - to_position[0])
            + abs(from_position[1] - to_position[1])
            != 1
        ):
            return False

        piece: Piece = self.game.board.get_piece(from_position)

        # Check if piece is owned by current player
        if self.game.current_turn != piece.owner:
            return False

        # Check if moving into own den
        own_den = (
            self.game.board.PLAYER_1_DEN_POSITION
            if self.game.current_turn == 0
            else self.game.board.PLAYER_2_DEN_POSITION
        )
        if to_position == own_den:
            return False

        # Check if non-rat piece trying to enter water
        if (
            piece.name != "Rat"
            and self.game.board.get_tile(to_position).tile_type == Tile.WATER
        ):
            return False

        return True

    def convert_to_coordinates(self, position):
        """Convert position string like 'A1' to tuple (column, row)"""
        column = ord(position[0].upper()) - ord("A")  # Convert 'A'-'G' to 0-6
        row = int(position[1]) - 1  # Convert '1'-'9' to 0-8
        return (column, row) if 0 <= column < 7 and 0 <= row < 9 else None

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
        """Check if the game has been won (den capture or all pieces captured)"""
        current_player = self.game.current_turn
        opponent = 1 - current_player
        opponent_den = (
            self.game.board.PLAYER_2_DEN_POSITION
            if current_player == 0
            else self.game.board.PLAYER_1_DEN_POSITION
        )

        # Win Condition 1: Player entered opponent's den
        if to_position == opponent_den:
            self.view.display_board(self.game.board)
            print(
                f"\n🎉 {self.game.players[current_player].name} wins by entering the opponent's den! 🎉"
            )
            return True

        # Win Condition 2: Opponent has no pieces left
        if self.count_player_pieces(opponent) == 0:
            self.view.display_board(self.game.board)
            print(
                f"\n🎉 {self.game.players[current_player].name} wins by capturing all opponent pieces! 🎉"
            )
            return True

        return False

    def count_player_pieces(self, player: int) -> int:
        """Count the number of pieces a player has on the board"""
        return sum(
            1
            for column in self.game.board.grid
            for tile in column
            if tile.get_piece() is not None and tile.get_piece().owner == player
        )
