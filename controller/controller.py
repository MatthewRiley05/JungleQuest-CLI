"""
Game Controller Module

This module contains the Controller class which manages game flow,
user input, move validation, and game state management.
"""

import re
import random
from typing import Optional

from model.game import Game
from model.board import Board
from model.tile import Tile
from model.piece import Piece
from view.view import View

from .move_parser import MoveParser
from .move_validator import MoveValidator
from .game_state import GameStateManager


class Controller:
    """
    Main game controller managing game flow and user interactions.

    Handles user input, move validation, game state management,
    undo functionality, and win condition checking.

    Attributes:
        RANDOM_NAMES: List of names for random player name generation
        MAX_UNDOS: Maximum number of undos allowed per game
        view: View instance for display operations
        game: Current game instance
        move_history: Stack of previous game states for undo
        undo_count: Number of undos used in current game
    """

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

    def __init__(self) -> None:
        """Initialize the controller with view and empty game state."""
        self.view = View()
        self.game = None

        self.move_parser = MoveParser()
        self.move_validator: Optional[MoveValidator] = None
        self.state_manager = GameStateManager(max_undos=3)

    def start_game(self) -> None:
        """
        Start a new game session.

        Displays welcome banner, prompts for player names,
        initializes the game, and starts the main game loop.
        """
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
        self.move_validator = MoveValidator(self.game.board)
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

    def play_game(self) -> None:
        """
        Main game loop.

        Continuously displays the board, gets user input, processes moves,
        and checks for win conditions until the game ends.
        """
        game_over = False
        while not game_over:
            self.view.display_board(self.game.board)
            self.view.display_turn(self.game.players[self.game.current_turn].name)

            # Display undo info
            print(
                f"Undos remaining: {self.state_manager.get_undos_remaining()}/{self.state_manager.MAX_UNDOS}"
            )

            move = self.view.get_user_input()
            if move.lower() == "quit":
                print("Terminating game session...")
                break

            # Handle undo command
            if move.lower() == "undo":
                if self.state_manager.undo_move(self.game.board, self.game):
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

    def take_turn(self, move):
        # Validate the move string format
        from_position, to_position = self.move_parser.parse_move_input(move)

        if not from_position or not to_position:
            return None  # for invalid inputs

        current_player = self.game.current_turn  # 0 for player 1, 1 for player 2
        piece_to_move: Piece = self.game.board.get_piece(from_position)

        if piece_to_move is None:
            print("Invalid move. A tile with no piece was selected. Please try again.")
            return None

        if not self.move_validator.is_valid_move(
            from_position, to_position, current_player
        ):
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
        self.state_manager._save_game_state(self.game.board, self.game.current_turn)

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
