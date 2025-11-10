from .board import Board
from .player import Player


class Game:
    def __init__(self, player1_name, player2_name):
        self.board = Board()
        self.players = [Player(player1_name), Player(player2_name)]
        self.current_turn = 0

    def switch_turn(self):
        """Switch to the next player's turn"""
        self.current_turn = (self.current_turn + 1) % 2
