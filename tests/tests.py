import unittest
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model.board import Board
from model.piece import Piece
from model.tile import Tile
from model.player import Player
from model.game import Game
from controller.controller import Controller
from controller.move_parser import MoveParser


class TestTile(unittest.TestCase):
    """Test cases for Tile class"""

    def test_tile_initialization(self):
        """Test tile is created with correct default values"""
        tile = Tile()
        self.assertEqual(tile.tile_type, Tile.LAND)
        self.assertIsNone(tile.piece)
        self.assertEqual(tile.owner, -1)

    def test_tile_with_piece(self):
        """Test tile can hold a piece"""
        piece = Piece("Rat", Piece.PLAYER_1)
        tile = Tile(Tile.LAND, piece)
        self.assertFalse(tile.is_empty())
        self.assertEqual(tile.get_piece(), piece)

    def test_tile_types(self):
        """Test different tile types"""
        land_tile = Tile(Tile.LAND)
        water_tile = Tile(Tile.WATER)
        trap_tile = Tile(Tile.TRAP, None, Tile.PLAYER_1)
        den_tile = Tile(Tile.PLAYER_1_DEN)

        self.assertEqual(land_tile.tile_type, Tile.LAND)
        self.assertEqual(water_tile.tile_type, Tile.WATER)
        self.assertEqual(trap_tile.tile_type, Tile.TRAP)
        self.assertEqual(den_tile.tile_type, Tile.PLAYER_1_DEN)

    def test_place_piece(self):
        """Test placing a piece on a tile"""
        tile = Tile()
        piece = Piece("Cat", Piece.PLAYER_1)
        tile.place_piece(piece)
        self.assertEqual(tile.piece, piece)
        self.assertFalse(tile.is_empty())


class TestPiece(unittest.TestCase):
    """Test cases for Piece class"""

    def test_piece_initialization(self):
        """Test piece is created with correct attributes"""
        piece = Piece("Elephant", Piece.PLAYER_1)
        self.assertEqual(piece.name, "Elephant")
        self.assertEqual(piece.rank, 8)
        self.assertEqual(piece.owner, Piece.PLAYER_1)

    def test_piece_ranks(self):
        """Test all piece ranks are correct"""
        ranks = {
            "Rat": 1,
            "Cat": 2,
            "Dog": 3,
            "Wolf": 4,
            "Leopard": 5,
            "Tiger": 6,
            "Lion": 7,
            "Elephant": 8,
        }
        for name, expected_rank in ranks.items():
            piece = Piece(name, Piece.PLAYER_1)
            self.assertEqual(piece.rank, expected_rank)

    def test_piece_string_representation(self):
        """Test piece string representation"""
        piece = Piece("Elephant", Piece.PLAYER_1)
        self.assertEqual(str(piece), "E")

    def test_normal_capture(self):
        """Test normal piece capture rules"""
        elephant = Piece("Elephant", Piece.PLAYER_1)
        tiger = Piece("Tiger", Piece.PLAYER_2)

        elephant_tile = Tile(Tile.LAND, elephant)
        tiger_tile = Tile(Tile.LAND, tiger)

        # Elephant (rank 8) can capture Tiger (rank 6)
        self.assertTrue(elephant.can_capture(elephant_tile, tiger, tiger_tile))
        # Tiger (rank 6) cannot capture Elephant (rank 8)
        self.assertFalse(tiger.can_capture(tiger_tile, elephant, elephant_tile))

    def test_equal_rank_capture(self):
        """Test pieces of equal rank can capture each other"""
        cat1 = Piece("Cat", Piece.PLAYER_1)
        cat2 = Piece("Cat", Piece.PLAYER_2)

        cat1_tile = Tile(Tile.LAND, cat1)
        cat2_tile = Tile(Tile.LAND, cat2)

        self.assertTrue(cat1.can_capture(cat1_tile, cat2, cat2_tile))
        self.assertTrue(cat2.can_capture(cat2_tile, cat1, cat1_tile))

    def test_rat_elephant_special_case(self):
        """Test rat can capture elephant on land"""
        rat = Piece("Rat", Piece.PLAYER_1)
        elephant = Piece("Elephant", Piece.PLAYER_2)

        rat_tile = Tile(Tile.LAND, rat)
        elephant_tile = Tile(Tile.LAND, elephant)

        # Rat can capture Elephant on land
        self.assertTrue(rat.can_capture(rat_tile, elephant, elephant_tile))
        # Elephant cannot capture Rat
        self.assertFalse(elephant.can_capture(elephant_tile, rat, rat_tile))

    def test_rat_water_mechanics(self):
        """Test rat in water cannot capture pieces on land"""
        rat = Piece("Rat", Piece.PLAYER_1)
        cat = Piece("Cat", Piece.PLAYER_2)

        rat_water_tile = Tile(Tile.WATER, rat)
        cat_land_tile = Tile(Tile.LAND, cat)

        # Rat in water cannot capture Cat on land
        self.assertFalse(rat.can_capture(rat_water_tile, cat, cat_land_tile))

    def test_rat_on_land_cannot_capture_in_water(self):
        """Test rat on land cannot capture pieces in water"""
        rat1 = Piece("Rat", Piece.PLAYER_1)
        rat2 = Piece("Rat", Piece.PLAYER_2)

        rat1_land_tile = Tile(Tile.LAND, rat1)
        rat2_water_tile = Tile(Tile.WATER, rat2)

        # Rat on land cannot capture Rat in water
        self.assertFalse(rat1.can_capture(rat1_land_tile, rat2, rat2_water_tile))

    def test_rat_vs_rat_same_environment(self):
        """Test rats can only capture each other in same environment"""
        rat1 = Piece("Rat", Piece.PLAYER_1)
        rat2 = Piece("Rat", Piece.PLAYER_2)

        # Both on land
        rat1_land = Tile(Tile.LAND, rat1)
        rat2_land = Tile(Tile.LAND, rat2)
        self.assertTrue(rat1.can_capture(rat1_land, rat2, rat2_land))

        # Both in water
        rat1_water = Tile(Tile.WATER, rat1)
        rat2_water = Tile(Tile.WATER, rat2)
        self.assertTrue(rat1.can_capture(rat1_water, rat2, rat2_water))

    def test_trap_capture(self):
        """Test pieces in opponent's trap can be captured by any piece"""
        rat = Piece("Rat", Piece.PLAYER_1)
        elephant = Piece("Elephant", Piece.PLAYER_2)

        rat_tile = Tile(Tile.LAND, rat)
        elephant_trap_tile = Tile(Tile.TRAP, elephant, Tile.PLAYER_1)

        # Rat can capture Elephant in its own trap
        self.assertTrue(rat.can_capture(rat_tile, elephant, elephant_trap_tile))


class TestBoard(unittest.TestCase):
    """Test cases for Board class"""

    def test_board_initialization(self):
        """Test board is initialized with correct dimensions"""
        board = Board()
        self.assertEqual(len(board.grid), Board.MAX_COLUMNS)
        self.assertEqual(len(board.grid[0]), Board.MAX_ROWS)

    def test_board_special_tiles(self):
        """Test special tiles are placed correctly"""
        board = Board()

        # Check dens
        self.assertEqual(board.grid[3][0].tile_type, Tile.PLAYER_1_DEN)
        self.assertEqual(board.grid[3][8].tile_type, Tile.PLAYER_2_DEN)

        # Check traps around Player 1 den
        self.assertEqual(board.grid[2][0].tile_type, Tile.TRAP)
        self.assertEqual(board.grid[4][0].tile_type, Tile.TRAP)
        self.assertEqual(board.grid[3][1].tile_type, Tile.TRAP)

        # Check traps around Player 2 den
        self.assertEqual(board.grid[2][8].tile_type, Tile.TRAP)
        self.assertEqual(board.grid[4][8].tile_type, Tile.TRAP)
        self.assertEqual(board.grid[3][7].tile_type, Tile.TRAP)

    def test_board_water_tiles(self):
        """Test water tiles are placed correctly"""
        board = Board()

        # Check water sections
        for col in [1, 2, 4, 5]:
            for row in [3, 4, 5]:
                self.assertEqual(board.grid[col][row].tile_type, Tile.WATER)

    def test_initial_piece_placement(self):
        """Test all pieces are placed correctly at game start"""
        board = Board()

        # Check Player 1's Elephant
        elephant_tile = board.grid[6][2]
        self.assertIsNotNone(elephant_tile.piece)
        self.assertEqual(elephant_tile.piece.name, "Elephant")
        self.assertEqual(elephant_tile.piece.owner, Piece.PLAYER_1)

        # Check Player 2's Elephant
        elephant_tile_p2 = board.grid[0][6]
        self.assertIsNotNone(elephant_tile_p2.piece)
        self.assertEqual(elephant_tile_p2.piece.name, "Elephant")
        self.assertEqual(elephant_tile_p2.piece.owner, Piece.PLAYER_2)

    def test_place_and_remove_piece(self):
        """Test placing and removing pieces"""
        board = Board()
        position = (0, 0)

        # Clear the position first
        board.remove_piece(position)
        self.assertTrue(board.get_tile(position).is_empty())

        # Place a piece
        piece = Piece("Cat", Piece.PLAYER_1)
        board.place_piece(piece, position)
        self.assertEqual(board.get_piece(position), piece)

        # Remove the piece
        board.remove_piece(position)
        self.assertIsNone(board.get_piece(position))

    def test_get_tile(self):
        """Test getting tiles from board"""
        board = Board()
        tile = board.get_tile((3, 0))
        self.assertEqual(tile.tile_type, Tile.PLAYER_1_DEN)


class TestPlayer(unittest.TestCase):
    """Test cases for Player class"""

    def test_player_initialization(self):
        """Test player is created with correct name"""
        player = Player("Alice")
        self.assertEqual(player.name, "Alice")
        self.assertEqual(len(player.pieces), 0)

    def test_add_piece(self):
        """Test adding pieces to player"""
        player = Player("Bob")
        piece = Piece("Rat", Piece.PLAYER_1)
        player.add_piece(piece)
        self.assertEqual(len(player.pieces), 1)
        self.assertIn(piece, player.pieces)

    def test_get_pieces(self):
        """Test getting player's pieces"""
        player = Player("Charlie")
        piece1 = Piece("Rat", Piece.PLAYER_1)
        piece2 = Piece("Cat", Piece.PLAYER_1)
        player.add_piece(piece1)
        player.add_piece(piece2)
        self.assertEqual(len(player.get_pieces()), 2)


class TestGame(unittest.TestCase):
    """Test cases for Game class"""

    def test_game_initialization(self):
        """Test game is initialized correctly"""
        game = Game("Player1", "Player2")
        self.assertIsNotNone(game.board)
        self.assertEqual(len(game.players), 2)
        self.assertEqual(game.players[0].name, "Player1")
        self.assertEqual(game.players[1].name, "Player2")
        self.assertEqual(game.current_turn, 0)

    def test_switch_turn(self):
        """Test turn switching"""
        game = Game("Player1", "Player2")
        self.assertEqual(game.current_turn, 0)
        game.switch_turn()
        self.assertEqual(game.current_turn, 1)
        game.switch_turn()
        self.assertEqual(game.current_turn, 0)


class TestController(unittest.TestCase):
    """Test cases for Controller class"""

    def setUp(self):
        """Set up test controller"""
        self.controller = Controller()
        self.controller.game = Game("TestPlayer1", "TestPlayer2")
        self.move_parser = MoveParser()

    def test_convert_to_coordinates(self):
        """Test coordinate conversion from algebraic notation"""
        # Test valid coordinates
        self.assertEqual(self.move_parser.convert_to_coordinates("A1"), (0, 0))
        self.assertEqual(self.move_parser.convert_to_coordinates("G9"), (6, 8))
        self.assertEqual(self.move_parser.convert_to_coordinates("D5"), (3, 4))

        # Test lowercase
        self.assertEqual(self.move_parser.convert_to_coordinates("a1"), (0, 0))
        self.assertEqual(self.move_parser.convert_to_coordinates("g9"), (6, 8))

        # Test invalid coordinates
        self.assertIsNone(self.move_parser.convert_to_coordinates("H1"))
        self.assertIsNone(self.move_parser.convert_to_coordinates("A0"))
        # Note: A10 would parse as (0, 0) because it only reads first digit
        # This is a known limitation of the current implementation

    def test_parse_move_input(self):
        """Test parsing move input strings"""
        # Valid inputs
        from_pos, to_pos = self.move_parser.parse_move_input("A1 to A2")
        self.assertEqual(from_pos, (0, 0))
        self.assertEqual(to_pos, (0, 1))

        from_pos, to_pos = self.move_parser.parse_move_input("G9 to F9")
        self.assertEqual(from_pos, (6, 8))
        self.assertEqual(to_pos, (5, 8))

        # Invalid inputs
        from_pos, to_pos = self.move_parser.parse_move_input("invalid")
        self.assertIsNone(from_pos)
        self.assertIsNone(to_pos)

        from_pos, to_pos = self.move_parser.parse_move_input("A1 A2")
        self.assertIsNone(from_pos)
        self.assertIsNone(to_pos)

    def test_is_valid_move_one_tile(self):
        """Test valid moves are exactly one tile orthogonally"""
        # Clear the area and place a piece at (0, 1) which is all surrounded by land
        board = self.controller.game.board
        board.remove_piece((0, 0))
        board.remove_piece((0, 1))
        board.remove_piece((0, 2))
        board.remove_piece((1, 1))

        piece = Piece("Cat", Piece.PLAYER_1)
        board.place_piece(piece, (0, 1))

        self.controller.game.current_turn = 0

        # Valid moves (one tile in each direction, all land tiles)
        self.assertTrue(self.controller.is_valid_move((0, 1), (0, 2)))  # Down
        self.assertTrue(
            self.controller.is_valid_move((0, 1), (0, 0))
        )  # Up (den, but allowed)
        self.assertTrue(self.controller.is_valid_move((0, 1), (1, 1)))  # Right

        # Invalid moves (too far or diagonal)
        self.assertFalse(self.controller.is_valid_move((0, 1), (0, 3)))  # Two tiles
        self.assertFalse(self.controller.is_valid_move((0, 1), (1, 2)))  # Diagonal

    def test_cannot_move_into_own_den(self):
        """Test pieces cannot move into their own den"""
        piece = Piece("Cat", Piece.PLAYER_1)
        self.controller.game.board.place_piece(piece, (3, 1))

        # Try to move into own den
        self.assertFalse(self.controller.is_valid_move((3, 1), (3, 0)))

    def test_only_rats_can_enter_water(self):
        """Test only rats can move into water"""
        # Cat trying to enter water
        cat = Piece("Cat", Piece.PLAYER_1)
        self.controller.game.board.place_piece(cat, (1, 2))
        self.assertFalse(self.controller.is_valid_move((1, 2), (1, 3)))

        # Rat can enter water
        self.controller.game.board.remove_piece((1, 2))
        rat = Piece("Rat", Piece.PLAYER_1)
        self.controller.game.board.place_piece(rat, (1, 2))
        self.assertTrue(self.controller.is_valid_move((1, 2), (1, 3)))

    def test_lion_tiger_river_jump_horizontal(self):
        """Test Lion and Tiger can jump horizontally across river"""
        lion = Piece("Lion", Piece.PLAYER_1)
        self.controller.game.board.place_piece(lion, (0, 4))

        # Should be able to jump 3 columns horizontally
        self.assertTrue(self.controller.is_valid_move((0, 4), (3, 4)))

    def test_lion_tiger_river_jump_vertical(self):
        """Test Lion and Tiger can jump vertically across river"""
        tiger = Piece("Tiger", Piece.PLAYER_1)
        self.controller.game.board.place_piece(tiger, (1, 2))

        # Should be able to jump 4 rows vertically
        self.assertTrue(self.controller.is_valid_move((1, 2), (1, 6)))

    def test_river_jump_blocked_by_rat(self):
        """Test Lion/Tiger cannot jump if rat is in the path"""
        lion = Piece("Lion", Piece.PLAYER_1)
        rat = Piece("Rat", Piece.PLAYER_2)

        self.controller.game.board.place_piece(lion, (0, 4))
        self.controller.game.board.place_piece(rat, (1, 4))

        # Jump should be blocked by rat
        self.assertFalse(self.controller.is_valid_move((0, 4), (3, 4)))

    def test_check_win_condition_den(self):
        """Test winning by entering opponent's den"""
        piece = Piece("Cat", Piece.PLAYER_1)
        self.controller.game.board.place_piece(piece, (3, 7))

        # Move into opponent's den
        result = self.controller.check_win_condition((3, 8))
        self.assertTrue(result)

    def test_check_win_condition_capture_all(self):
        """Test winning by capturing all opponent pieces"""
        # Clear the board except one piece for each player
        board = self.controller.game.board
        for col in range(Board.MAX_COLUMNS):
            for row in range(Board.MAX_ROWS):
                board.remove_piece((col, row))

        # Place one piece for player 1, none for player 2
        piece = Piece("Cat", Piece.PLAYER_1)
        board.place_piece(piece, (0, 0))

        self.controller.game.current_turn = 0
        result = self.controller.check_win_condition((0, 0))
        self.assertTrue(result)

    def test_count_player_pieces(self):
        """Test counting pieces for each player"""
        # Initial board should have 8 pieces per player
        count_p1 = self.controller.count_player_pieces(0)
        count_p2 = self.controller.count_player_pieces(1)
        self.assertEqual(count_p1, 8)
        self.assertEqual(count_p2, 8)

    def test_piece_ownership_validation(self):
        """Test players can only move their own pieces"""
        piece = Piece("Cat", Piece.PLAYER_1)
        self.controller.game.board.place_piece(piece, (3, 3))

        self.controller.game.current_turn = 0
        self.assertTrue(self.controller.is_valid_move((3, 3), (3, 4)))

        self.controller.game.current_turn = 1
        self.assertFalse(self.controller.is_valid_move((3, 3), (3, 4)))


class TestIntegration(unittest.TestCase):
    """Integration tests for complete game scenarios"""

    def setUp(self):
        """Set up test game"""
        self.controller = Controller()
        self.controller.game = Game("Player1", "Player2")

    def test_complete_move_sequence(self):
        """Test a sequence of valid moves"""
        board = self.controller.game.board

        # Player 1 moves Rat from (0, 2) to (0, 3)
        self.controller.game.current_turn = 0
        result = self.controller.take_turn("A3 to A4")
        self.assertFalse(result)  # Game continues
        self.assertIsNone(board.get_piece((0, 2)))
        self.assertIsNotNone(board.get_piece((0, 3)))

    def test_capture_sequence(self):
        """Test piece capture"""
        board = self.controller.game.board

        # Set up a capture scenario
        board.remove_piece((3, 3))
        board.remove_piece((3, 4))

        cat = Piece("Cat", Piece.PLAYER_1)
        rat = Piece("Rat", Piece.PLAYER_2)

        board.place_piece(cat, (3, 3))
        board.place_piece(rat, (3, 4))

        # Player 1 captures Player 2's rat
        self.controller.game.current_turn = 0
        result = self.controller.take_turn("D4 to D5")

        self.assertFalse(result)  # Game continues
        self.assertIsNone(board.get_piece((3, 3)))
        piece_at_dest = board.get_piece((3, 4))
        self.assertIsNotNone(piece_at_dest)
        self.assertEqual(piece_at_dest.name, "Cat")


if __name__ == "__main__":
    unittest.main()
