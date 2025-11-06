from model.game import Game
from model.piece import Piece
from model.tile import Tile

from view.view import View


class Controller:
    def __init__(self):
        self.view = View()
        self.game = None

    def start_game(self):
        print("Starting game...")
        player1_name = input("Enter name for Player 1: ")
        player2_name = input("Enter name for Player 2: ")
        self.game = Game(player1_name, player2_name)
        self.game.setup_game()
        self.play_game()

    def play_game(self):
        while True:
            self.view.display_board(self.game.board)
            self.view.display_turn(self.game.players[self.game.current_turn].name)

            move = self.view.get_user_input()
            if move.lower() == 'quit':
                break
            
            # Here will be implement move processing logic
            # WIP
            # This is where you would call game methods to update the board
            self.game.switch_turn()
    
    # WIP: TURN LOGIC
    def take_turn(self, from_position, to_position):
        current_player = self.game.players[self.game.current_turn]
        piece_to_move = self.game.board.get_piece(from_position)

        # Validate that the piece belongs to the current player
        if piece_to_move is None or piece_to_move.color != current_player.color:
            print("Invalid move: You can only move your own pieces.")
            return

        # Validate the move is within the board limits and to a valid tile
        if not self.is_valid_move(from_position, to_position):
            print("Invalid move: Move is not allowed.")
            return

        # Check if the target tile is occupied
        target_tile = self.game.board.get_piece(to_position)
        if target_tile is not None:
            if target_tile.color == current_player.color:
                print("Invalid move: You cannot move to a tile occupied by your own piece.")
                return
            else:
                # Capture logic: remove the opponent's piece
                self.capture_piece(to_position)

        # Move the piece
        self.game.board.place_piece(piece_to_move, to_position)
        self.game.board.get_tile(from_position).remove_piece()  # Remove from original position

        # End the turn
        self.end_turn()