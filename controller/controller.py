from model.game import Game
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