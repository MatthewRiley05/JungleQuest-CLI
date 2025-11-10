"""
Game constants and configuration values.
Centralizes all magic numbers and shared constants.
"""

# Player identifiers
PLAYER_1 = 0
PLAYER_2 = 1
NEUTRAL = -1

# Board dimensions
BOARD_COLUMNS = 7
BOARD_ROWS = 9

# Board positions
PLAYER_1_DEN_POSITION = (3, 0)
PLAYER_2_DEN_POSITION = (3, 8)

# Piece ranks
PIECE_RANKS = {
    "Rat": 1,
    "Cat": 2,
    "Dog": 3,
    "Wolf": 4,
    "Leopard": 5,
    "Tiger": 6,
    "Lion": 7,
    "Elephant": 8,
}

# Piece abbreviations for display
PIECE_ABBREVIATIONS = {
    "Rat": "rat",
    "Cat": "cat",
    "Dog": "dog",
    "Wolf": "wlf",
    "Leopard": "lpd",
    "Tiger": "tgr",
    "Lion": "lio",
    "Elephant": "elp",
}

# Tile types
TILE_LAND = "L"
TILE_PLAYER_1_DEN = "D1"
TILE_PLAYER_2_DEN = "D2"
TILE_TRAP = "T"
TILE_WATER = "W"

# Tile display symbols
TILE_SYMBOLS = {
    TILE_LAND: "  ",
    TILE_PLAYER_1_DEN: "D1",
    TILE_PLAYER_2_DEN: "D2",
    TILE_TRAP: "TR",
    TILE_WATER: "~~",
}

# River positions (for jumping logic)
LEFT_RIVER_COLS = (1, 2)
RIGHT_RIVER_COLS = (4, 5)
RIVER_COL_SPAN = 3  # Distance to jump across river horizontally
RIVER_ROW_SPAN = 4  # Distance to jump across river vertically

# Move validation
MAX_MOVE_DISTANCE = 1  # Normal pieces can only move 1 tile
