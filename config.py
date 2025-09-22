from dataclasses import dataclass, field

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
# BoardState = tuple[list[int], list[int], list[int], list[int], int, int]

# CastlingState = tuple[bool, bool, bool]


# PieceMoves = tuple[list[tuple[int, int]], list[list[int]]] | None
@dataclass
class Piece:
    piece: int
    index: int


@dataclass
class PieceMoves:
    pieces: list[Piece] = field(default_factory=list)
    move_list: list[list[int]] = field(default_factory=list)


@dataclass
class CastlingState:
    white_kingside: bool = True
    white_queenside: bool = True
    black_kingside: bool = True
    black_queenside: bool = True

    def can_castle_kingside(self, color: int) -> bool:
        return self.white_kingside if color == WHITE else self.black_kingside

    def can_castle_queenside(self, color: int) -> bool:
        return self.white_queenside if color == WHITE else self.black_queenside

    def disable_kingside(self, color: int):
        if color == WHITE:
            self.white_kingside = False
        else:
            self.black_kingside = False

    def disable_queenside(self, color: int):
        if color == WHITE:
            self.white_queenside = False
        else:
            self.black_queenside = False

    def disable_all(self, color: int):
        if color == WHITE:
            self.disable_kingside(WHITE)
            self.disable_queenside(WHITE)
        else:
            self.disable_kingside(BLACK)
            self.disable_queenside(BLACK)
