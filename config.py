EMPTY_SQUARE = 0
PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING = 1, 2, 3, 4, 5, 6

WHITE_PAWN, WHITE_KNIGHT, WHITE_BISHOP, WHITE_ROOK, WHITE_QUEEN, WHITE_KING = (
    1,
    2,
    3,
    4,
    5,
    6,
)
BLACK_PAWN, BLACK_KNIGHT, BLACK_BISHOP, BLACK_ROOK, BLACK_QUEEN, BLACK_KING = (
    -1,
    -2,
    -3,
    -4,
    -5,
    -6,
)

WHITE = 1
BLACK = 0

# Alias for BoardState type used in the `find_pieces` function
BoardState = tuple[list[int], list[int], list[int], list[int], int, int]
