from model.game import Game
from model.board import Board
from model.tile import Tile
from model.piece import Piece
from view.view import View

import re
import random
import json
import os
from datetime import datetime


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
        self.move_record = []  # List to store all moves for recording to .record file
        self.recording_enabled = True  # Enable recording by default

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

        # Main menu
        while True:
            print("\n" + "=" * 60)
            print("MAIN MENU")
            print("=" * 60)
            print("1. New Game")
            print("2. Load Game (.jungle)")
            print("3. Replay Game (.record)")
            print("4. Quit")
            print("=" * 60)

            choice = input("Enter your choice (1-4): ").strip()

            if choice == "1":
                self._new_game()
                break
            elif choice == "2":
                if self._load_game_menu():
                    break
            elif choice == "3":
                self._replay_game_menu()
            elif choice == "4":
                print("Thanks for playing Jungle Quest! Goodbye!")
                return
            else:
                print("Invalid choice. Please enter 1, 2, 3, or 4.")

    def _new_game(self):
        """Start a new game with player name input."""
        player1_name = self._get_valid_player_name("Player 1")
        player2_name = self._get_valid_player_name("Player 2")
        self.game = Game(player1_name, player2_name)
        self.move_record = []  # Reset move record for new game
        self.move_history = []  # Reset undo history
        self.undo_count = 0  # Reset undo count
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
            move_lower = move.lower().strip()

            if move_lower == "quit":
                if self._confirm_quit():
                    print("Terminating game session...")
                    break
                else:
                    continue

            # Handle save command
            if move_lower == "save":
                self._save_game_menu()
                continue

            # Handle record command
            if move_lower == "record":
                self._save_record_menu()
                continue

            # Handle undo command
            if move_lower == "undo":
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
                # Auto-save record on game completion
                self._auto_save_record()
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

        # Record the move for .record file
        if self.recording_enabled:
            self._record_move(
                move, from_position, to_position, piece_to_move, target_piece
            )

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
                    board_state[(col, row)] = {"name": piece.name, "owner": piece.owner}

        # Save state with current player turn
        state = {"board": board_state, "current_turn": self.game.current_turn}
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

        # Also remove the last move from the record
        if self.move_record:
            self.move_record.pop()

        # Clear the current board
        for row in range(9):
            for col in range(7):
                self.game.board.remove_piece((col, row))

        # Restore pieces to their previous positions
        for position, piece_info in previous_state["board"].items():
            # Recreate the piece
            piece = Piece(piece_info["name"], piece_info["owner"])
            self.game.board.place_piece(piece, position)

        # Restore the turn
        self.game.current_turn = previous_state["current_turn"]

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

    # ==================== FILE I/O METHODS ====================

    def _confirm_quit(self) -> bool:
        """Ask user to confirm quitting and offer to save."""
        print("\nAre you sure you want to quit?")
        print("1. Save and quit")
        print("2. Quit without saving")
        print("3. Cancel (continue playing)")

        choice = input("Enter your choice (1-3): ").strip()

        if choice == "1":
            self._save_game_menu()
            return True
        elif choice == "2":
            return True
        else:
            print("Continuing game...")
            return False

    def _record_move(
        self,
        move_str: str,
        from_pos: tuple,
        to_pos: tuple,
        piece: Piece,
        captured_piece: Piece = None,
    ):
        """Record a move to the move_record list."""
        move_data = {
            "move_number": len(self.move_record) + 1,
            "player": self.game.players[self.game.current_turn].name,
            "player_index": self.game.current_turn,
            "move_string": move_str,
            "piece": piece.name,
            "from": self._coords_to_notation(from_pos),
            "to": self._coords_to_notation(to_pos),
            "captured": captured_piece.name if captured_piece else None,
            "timestamp": datetime.now().isoformat(),
        }
        self.move_record.append(move_data)

    def _coords_to_notation(self, coords: tuple[int, int]) -> str:
        """Convert (col, row) coordinates to chess-like notation (e.g., A1)."""
        col, row = coords
        return f"{chr(ord('A') + col)}{row + 1}"

    def _notation_to_coords(self, notation: str) -> tuple[int, int]:
        """Convert chess-like notation (e.g., A1) to (col, row) coordinates."""
        col = ord(notation[0].upper()) - ord("A")
        row = int(notation[1]) - 1
        return (col, row)

    # ==================== SAVE/LOAD GAME (.jungle files) ====================

    def _save_game_menu(self):
        """Prompt user for filename and save current game state."""
        filename = input("Enter filename to save (without extension): ").strip()
        if not filename:
            print("Save cancelled.")
            return

        if not filename.endswith(".jungle"):
            filename += ".jungle"

        try:
            self._save_game(filename)
            print(f"✓ Game saved successfully to '{filename}'")
        except Exception as e:
            print(f"✗ Error saving game: {e}")

    def _save_game(self, filename: str):
        """Save the current game state to a .jungle file."""
        # Serialize board state
        board_state = {}
        for row in range(9):
            for col in range(7):
                tile = self.game.board.get_tile((col, row))
                piece = tile.get_piece()
                if piece:
                    board_state[f"{col},{row}"] = {
                        "name": piece.name,
                        "owner": piece.owner,
                    }

        # Create game data structure
        game_data = {
            "version": "1.0",
            "timestamp": datetime.now().isoformat(),
            "players": [p.name for p in self.game.players],
            "current_turn": self.game.current_turn,
            "undo_count": self.undo_count,
            "board": board_state,
            "move_record": self.move_record,
            "move_history": [
                {
                    "board": {f"{k[0]},{k[1]}": v for k, v in state["board"].items()},
                    "current_turn": state["current_turn"],
                }
                for state in self.move_history
            ],
        }

        # Write to file
        with open(filename, "w") as f:
            json.dump(game_data, f, indent=2)

    def _load_game_menu(self) -> bool:
        """Prompt user for filename and load game state."""
        filename = input("Enter filename to load (without extension): ").strip()
        if not filename:
            print("Load cancelled.")
            return False

        if not filename.endswith(".jungle"):
            filename += ".jungle"

        if not os.path.exists(filename):
            print(f"✗ File '{filename}' not found.")
            return False

        try:
            self._load_game(filename)
            print(f"✓ Game loaded successfully from '{filename}'")
            self.play_game()
            return True
        except Exception as e:
            print(f"✗ Error loading game: {e}")
            return False

    def _load_game(self, filename: str):
        """Load game state from a .jungle file."""
        with open(filename, "r") as f:
            game_data = json.load(f)

        # Create new game with saved player names
        player_names = game_data["players"]
        self.game = Game(player_names[0], player_names[1])

        # Clear the board
        for row in range(9):
            for col in range(7):
                self.game.board.remove_piece((col, row))

        # Restore pieces
        for pos_str, piece_data in game_data["board"].items():
            col, row = map(int, pos_str.split(","))
            piece = Piece(piece_data["name"], piece_data["owner"])
            self.game.board.place_piece(piece, (col, row))

        # Restore game state
        self.game.current_turn = game_data["current_turn"]
        self.undo_count = game_data.get("undo_count", 0)
        self.move_record = game_data.get("move_record", [])

        # Restore move history for undo
        self.move_history = []
        for state_data in game_data.get("move_history", []):
            board_state = {}
            for pos_str, piece_data in state_data["board"].items():
                col, row = map(int, pos_str.split(","))
                board_state[(col, row)] = piece_data

            self.move_history.append(
                {"board": board_state, "current_turn": state_data["current_turn"]}
            )

    # ==================== RECORD/REPLAY (.record files) ====================

    def _save_record_menu(self):
        """Prompt user for filename and save game record."""
        if not self.move_record:
            print("No moves have been made yet. Nothing to record.")
            return

        filename = input("Enter filename to save record (without extension): ").strip()
        if not filename:
            print("Record save cancelled.")
            return

        if not filename.endswith(".record"):
            filename += ".record"

        try:
            self._save_record(filename)
            print(f"✓ Game record saved successfully to '{filename}'")
        except Exception as e:
            print(f"✗ Error saving record: {e}")

    def _save_record(self, filename: str):
        """Save game record to a .record file."""
        record_data = {
            "version": "1.0",
            "timestamp": datetime.now().isoformat(),
            "players": [p.name for p in self.game.players],
            "total_moves": len(self.move_record),
            "moves": self.move_record,
        }

        with open(filename, "w") as f:
            json.dump(record_data, f, indent=2)

    def _auto_save_record(self):
        """Automatically save game record when game ends."""
        if not self.move_record:
            return

        print("\nWould you like to save a record of this game? (y/n): ", end="")
        choice = input().strip().lower()

        if choice == "y":
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"game_record_{timestamp}.record"
            try:
                self._save_record(filename)
                print(f"✓ Game record saved to '{filename}'")
            except Exception as e:
                print(f"✗ Error saving record: {e}")

    def _replay_game_menu(self):
        """Prompt user for filename and replay game from record."""
        filename = input("Enter filename to replay (without extension): ").strip()
        if not filename:
            print("Replay cancelled.")
            return

        if not filename.endswith(".record"):
            filename += ".record"

        if not os.path.exists(filename):
            print(f"✗ File '{filename}' not found.")
            return

        try:
            self._replay_game(filename)
        except Exception as e:
            print(f"✗ Error replaying game: {e}")

    def _replay_game(self, filename: str):
        """Replay a game from a .record file."""
        with open(filename, "r") as f:
            record_data = json.load(f)

        # Create new game with recorded player names
        player_names = record_data["players"]
        self.game = Game(player_names[0], player_names[1])

        print("\n" + "=" * 60)
        print("GAME REPLAY MODE")
        print("=" * 60)
        print(f"Players: {player_names[0]} vs {player_names[1]}")
        print(f"Total moves: {record_data['total_moves']}")
        print(f"Recorded on: {record_data['timestamp']}")
        print("=" * 60)
        print("\nPress Enter to advance to next move, 'q' to quit replay.\n")

        # Show initial board
        self.view.display_board(self.game.board)

        # Replay each move
        for move_data in record_data["moves"]:
            user_input = input(f"\nMove {move_data['move_number']}: ").strip().lower()
            if user_input == "q":
                print("Replay stopped.")
                break

            # Display move info
            print(
                f"\n{move_data['player']} moves {move_data['piece']}: {move_data['move_string']}"
            )
            if move_data.get("captured"):
                print(f"  → Captured {move_data['captured']}!")

            # Execute the move
            from_pos = self._notation_to_coords(move_data["from"])
            to_pos = self._notation_to_coords(move_data["to"])

            piece = self.game.board.get_piece(from_pos)
            if piece:
                self.game.board.remove_piece(from_pos)
                # Remove captured piece if any
                if move_data.get("captured"):
                    self.game.board.remove_piece(to_pos)
                self.game.board.place_piece(piece, to_pos)

            # Update turn
            self.game.current_turn = move_data["player_index"]

            # Display updated board
            self.view.display_board(self.game.board)

        print("\n" + "=" * 60)
        print("Replay complete!")
        print("=" * 60)