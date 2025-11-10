from .board import Board
from .player import Player
from .piece import Piece


class Game:
    def __init__(self, player1_name, player2_name):
        self.board = Board()
        self.players = [Player(player1_name), Player(player2_name)]
        self.current_turn = 0

    def switch_turn(self):
        self.current_turn = (self.current_turn + 1) % 2

    def display_status(self):
        self.board.display_board()
        print(f"Current turn: {self.players[self.current_turn].name}")
