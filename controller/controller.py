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
        while True:
            self.view.display_board(self.game.board)
            self.view.display_turn(self.game.players[self.game.current_turn].name)

            move = self.view.get_user_input()
            if move.lower() == 'quit':
                print("Terminating game session...")
                break

            # Attempt to take the turn
            if not self.take_turn(move):  
                continue  # await new input from the user
            

            self.game.switch_turn()
    
    def parse_move_input(self, input : str):
        pattern = r'^[A-Ga-g][1-9] to [A-Ga-g][1-9]$' # valid characters include A-G, a-g, 1-9
        
        if not re.match(pattern, input):
            print("Invalid input format. Please enter a valid move (e.g: A1 to A2, B4 to C4)")
            return None, None # means input is invalid.
        
        from_part, to_part = input.split(" to ")

        if not self.convert_to_coordinates(from_part) or not self.convert_to_coordinates(to_part):
            print("Input is out of bounds. Please enter a valid move (e.g: A1 to A2, B4 to C4)")
            return None, None
        from_position = self.convert_to_coordinates(from_part)
        to_position = self.convert_to_coordinates(to_part)

        return from_position, to_position
    
    def is_valid_move(self, from_position : tuple[int, int], to_position : tuple[int, int]) -> bool: 
        row_difference = abs(from_position[0] - to_position[0])
        col_difference = abs(from_position[1] - to_position[1])
        
        # Check if the movement is only one tile upwards, downwards, left or right.
        if (row_difference + col_difference != 1):  
            return False
        
        piece : Piece = self.game.board.get_piece(from_position)
        # Check if the piece is owned by the current player. 
        # note: current_turn = 0 if player 1's turn, 1 if player 2's turn.
        if self.game.current_turn != piece.owner and (self.game.current_turn != piece.owner):
            return False 
        
        # Check if the move leads to the player's own den
        if self.game.current_turn == 0 and to_position == self.game.board.PLAYER_1_DEN_POSITION:
            return False
        if self.game.current_turn == 1 and to_position == self.game.board.PLAYER_2_DEN_POSITION:
            return False

        return True
    
    def convert_to_coordinates(self, position):
        # Convert a position string like "A1" to a tuple (row, column)
        # column = ord(position[0].upper()) - ord('A')  # Convert 'A'-'G' to 0-6
        # row = int(position[1]) - 1  # Convert '1'-'9' to 0-8
        # return (row, column) if 0 <= row < 7 and 0 <= column < 9 else (None, None)
        column = -1
        row = -1
        match position[0].upper():
            case 'A': column = 0
            case 'B': column = 1
            case 'C': column = 2
            case 'D': column = 3
            case 'E': column = 4
            case 'F': column = 5
            case 'G': column = 6
        row = int(position[1]) - 1 
        return (column, row)
    

    
    def take_turn(self, move):
        # Validate the move string format
        from_position, to_position = self.parse_move_input(move)


        if not from_position or not to_position:
            return  # for invalid inputs

        current_player = self.game.current_turn # 0 for player 1, 1 for player 2
        piece_to_move : Piece = self.game.board.get_piece(from_position)

        if piece_to_move is None:
            print("Invalid move. A tile with no piece was selected. Please try again.")
            return
        
        if self.is_valid_move(from_position, to_position) == False:
            print("Invalid move. You may only move your own piece by one tile horizontally/vertically, and never into your its own den.")
            return 

        # Check if the target tile is occupied
        target_tile : Tile = self.game.board.get_tile(to_position)
        if target_tile != None:
            if target_tile.get_piece() != None and ():
                print("Invalid move: You cannot move to a tile occupied by your own piece.")
                return
            # WIP
            # else:
            #     # Capture logic: remove the opponent's piece
            #     self.capture_piece(to_position)

        # Move the piece

        self.game.board.remove_piece(from_position)
        self.game.board.place_piece(piece_to_move, to_position)

        # End the turn
        self.end_turn()
    
    # WIP
    def capture_piece(self, position):
        # Logic to handle capturing an opponent's piece
        print(f"Captured piece at {position}")

    def end_turn(self):
        # Switch to the next player
        self.game.current_turn = (self.game.current_turn + 1) % len(self.game.players)
        print(f"{self.game.players[self.game.current_turn].name}'s turn.")