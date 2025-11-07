from model.board import Board

class View:
    def display_board(self, board : Board):
        print("\n")
        print("========================================== BOARD ==========================================")
        for i in range(board.MAX_ROWS):
            for j in range(board.MAX_COLUMNS):
                print(board.grid[j][i].__str__(), end=" ")
            print('\n')


    def display_turn(self, player_name):
        print(f"Current turn: {player_name}")

    def get_user_input(self):
        return input("Enter your move (e.g., 'A1 to B2') or 'quit' to terminate.: ")

    def display_message(self, message):
        print(message)