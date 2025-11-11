from model.game import Game
from model.board import Board
from model.tile import Tile
from model.piece import Piece
from view.view import View

import re
import random


class Controller:
    # List of random names for player name generation
    RANDOM_NAMES = [
        "Alpha",
        "Bravo",
        "Charlie",
        "Delta",
        "Echo",
        "Foxtrot",
        "Golf",
        "Hotel",
        "India",
        "Juliet",
        "Kilo",
        "Lima",
        "Mike",
        "November",
        "Oscar",
        "Papa",
        "Quebec",
        "Romeo",
        "Sierra",
        "Tango",
        "Uniform",
        "Victor",
        "Whiskey",
        "X-ray",
        "Yankee",
        "Zulu",
        "Ace",
        "Blaze",
        "Cipher",
        "Drake",
        "Ember",
        "Frost",
        "Ghost",
        "Hunter",
        "Iron",
        "Jade",
        "Knight",
        "Luna",
        "Maverick",
        "Nova",
        "Phoenix",
        "Raven",
        "Shadow",
        "Storm",
        "Tiger",
        "Viper",
        "Wolf",
        "Zen",
    ]

    def __init__(self):
        self.view = View()
        self.game = None
        self.move_history = []  # Stack to store move history for undo
        self.undo_count = 0  # Track number of undos used (max 3 per game)
        self.MAX_UNDOS = 3

    def start_game(self):
        print(
            r"""
     ██╗██╗   ██╗███╗   ██╗ ██████╗ ██╗     ███████╗     ██████╗  █████╗ ███╗   ███╗███████╗
     ██║██║   ██║████╗  ██║██╔════╝ ██║     ██╔════╝    ██╔════╝ ██╔══██╗████╗ ████║██╔════╝
     ██║██║   ██║██╔██╗ ██║██║  ███╗██║     █████╗      ██║  ███╗███████║██╔████╔██║█████╗  
██   ██║██║   ██║██║╚██╗██║██║   ██║██║     ██╔══╝      ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝  
╚█████╔╝╚██████╔╝██║ ╚████║╚██████╔╝███████╗███████╗    ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗
 ╚════╝  ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚══════╝     ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝
            """
        )
        player1_name = self._get_valid_player_name("Player 1")
        player2_name = self._get_valid_player_name("Player 2")
        self.game = Game(player1_name, player2_name)
        self.play_game()

    def _get_valid_player_name(self, player_label: str) -> str:
        """Prompt for a valid player name (non-empty, not just whitespace).

        Players can either:
        - Enter a custom name
        - Press Enter to get a randomly generated name
        """
        while True:
            name = input(
                f"Enter name for {player_label} (or press Enter for random name): "
            ).strip()
            if name:
                return name
            else:
                # Generate random name if user pressed Enter
                random_name = random.choice(self.RANDOM_NAMES)
                print(f"Random name generated: {random_name}")
                return random_name

    def play_game(self):
        game_over = False
        while not game_over:
            self.view.display_board(self.game.board)
            self.view.display_turn(self.game.players[self.game.current_turn].name)
            
            # Display undo info
            undos_remaining = self.MAX_UNDOS - self.undo_count
            print(f"Undos remaining: {undos_remaining}/{self.MAX_UNDOS}")

            move = self.view.get_user_input()
            if move.lower() == "quit":
                print("Terminating game session...")
                break
            
            # Handle undo command
            if move.lower() == "undo":
                if self.undo_move():
                    continue  # Successfully undone, show board again
                else:
                    continue  # Undo failed, show error and await new input

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

    def _is_river_jump_clear(self, from_pos, to_pos, is_horizontal):
        """Check if river jump path is clear of rats."""
        if is_horizontal:
            col_range = range(
                min(from_pos[0], to_pos[0]) + 1, max(from_pos[0], to_pos[0])
            )
            return all(
                self.game.board.get_tile((col, from_pos[1])).tile_type == Tile.WATER
                and self.game.board.get_tile((col, from_pos[1])).is_empty()
                for col in col_range
            )
        else:
            row_range = range(
                min(from_pos[1], to_pos[1]) + 1, max(from_pos[1], to_pos[1])
            )
            return all(
                self.game.board.get_tile((from_pos[0], row)).tile_type == Tile.WATER
                and self.game.board.get_tile((from_pos[0], row)).is_empty()
                for row in row_range
            )

    def is_valid_move(
        self, from_position: tuple[int, int], to_position: tuple[int, int]
    ) -> bool:
        piece: Piece = self.game.board.get_piece(from_position)

        # Lion/Tiger river jumping (3 cols horizontal or 4 rows vertical)
        if piece.name in ["Lion", "Tiger"]:
            from_col, from_row = from_position
            to_col, to_row = to_position
            if (
                from_row == to_row
                and abs(from_col - to_col) == 3
                and self._is_river_jump_clear(from_position, to_position, True)
            ):
                return True
            if (
                from_col == to_col
                and abs(from_row - to_row) == 4
                and self._is_river_jump_clear(from_position, to_position, False)
            ):
                return True

        # Check piece ownership
        if self.game.current_turn != piece.owner:
            return False

        # Prevent moving into own den
        own_den = (
            self.game.board.PLAYER_1_DEN_POSITION
            if self.game.current_turn == 0
            else self.game.board.PLAYER_2_DEN_POSITION
        )
        if to_position == own_den:
            return False

        # Only rats can enter water
        if (
            piece.name != "Rat"
            and self.game.board.get_tile(to_position).tile_type == Tile.WATER
        ):
            return False

        # Must move exactly one tile (orthogonal)
        return (
            abs(from_position[0] - to_position[0])
            + abs(from_position[1] - to_position[1])
            == 1
        )

    def convert_to_coordinates(self, position):
        column = ord(position[0].upper()) - ord("A")
        row = int(position[1]) - 1
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

        # Save game state before making the move (for undo functionality)
        self._save_game_state()

        # Move piece
        self.game.board.remove_piece(from_position)
        self.game.board.place_piece(piece_to_move, to_position)

        # Check for win conditions
        if self.check_win_condition(to_position):
            return True

        # Valid move, game continues
        return False

    def check_win_condition(self, to_position: tuple[int, int]) -> bool:
        current_player = self.game.current_turn
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
        if self.count_player_pieces(1 - current_player) == 0:
            self.view.display_board(self.game.board)
            print(
                f"\n🎉 {self.game.players[current_player].name} wins by capturing all opponent pieces! 🎉"
            )
            return True

        return False

    def _save_game_state(self):
        """Save the current game state before a move for potential undo."""
        # Create a deep copy of the board state
        board_state = {}
        for row in range(9):
            for col in range(7):
                tile = self.game.board.get_tile((col, row))
                piece = tile.get_piece()
                if piece:
                    # Store piece info: (name, owner, position)
                    board_state[(col, row)] = {
                        'name': piece.name,
                        'owner': piece.owner
                    }
        
        # Save state with current player turn
        state = {
            'board': board_state,
            'current_turn': self.game.current_turn
        }
        self.move_history.append(state)

    def undo_move(self):
        """Undo the last move if undos are available."""
        # Check if undos are available
        if self.undo_count >= self.MAX_UNDOS:
            print(f"Cannot undo: Maximum of {self.MAX_UNDOS} undos per game reached.")
            return False
        
        # Check if there's any move to undo
        if len(self.move_history) == 0:
            print("Cannot undo: No moves have been made yet.")
            return False
        
        # Restore the previous state
        previous_state = self.move_history.pop()
        
        # Clear the current board
        for row in range(9):
            for col in range(7):
                self.game.board.remove_piece((col, row))
        
        # Restore pieces to their previous positions
        for position, piece_info in previous_state['board'].items():
            # Recreate the piece
            piece = Piece(piece_info['name'], piece_info['owner'])
            self.game.board.place_piece(piece, position)
        
        # Restore the turn
        self.game.current_turn = previous_state['current_turn']
        
        # Increment undo counter
        self.undo_count += 1
        
        print(f"✓ Move undone! ({self.MAX_UNDOS - self.undo_count} undos remaining)")
        return True

    def count_player_pieces(self, player: int) -> int:
        return sum(
            1
            for column in self.game.board.grid
            for tile in column
            if tile.get_piece() and tile.get_piece().owner == player
        )

    def end_turn(self):
        # Switch to the next player
        self.game.current_turn = (self.game.current_turn + 1) % len(self.game.players)
        print(f"Now is {self.game.players[self.game.current_turn].name}'s turn.")
