from dataclasses import dataclass, field

###########################
# ------ CONSTANTS ------ #
###########################

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

FEN_CONVERSION = {
    "P": WHITE_PAWN,
    "p": BLACK_PAWN,
    "N": WHITE_KNIGHT,
    "n": BLACK_KNIGHT,
    "B": WHITE_BISHOP,
    "b": BLACK_BISHOP,
    "R": WHITE_ROOK,
    "r": BLACK_ROOK,
    "Q": WHITE_QUEEN,
    "q": BLACK_QUEEN,
    "K": WHITE_KING,
    "k": BLACK_KING,
}

BOARD_TO_FEN = {v: k for k, v in FEN_CONVERSION.items()}

###########################
# ------ DATACLASS ------ #
###########################


@dataclass
class Piece:
    piece: int
    index: int


@dataclass
class Move:
    piece: Piece
    to_idx: int

    def __iter__(self):
        return self.piece, self.to_idx


@dataclass
class PieceMoves:
    pieces: list[Piece] = field(default_factory=list)
    move_list: list[list[int]] = field(default_factory=list)

    def __bool__(self) -> bool:
        return len(self.pieces) > 0


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

    def to_fen(self) -> str:
        fen: str = ""
        if self.white_kingside:
            fen += "K"
        if self.white_queenside:
            fen += "Q"
        if self.black_kingside:
            fen += "k"
        if self.black_queenside:
            fen += "q"
        return fen or "-"

    def copy(self) -> "CastlingState":
        return CastlingState(
            white_kingside=self.white_kingside,
            white_queenside=self.white_queenside,
            black_kingside=self.black_kingside,
            black_queenside=self.black_queenside,
        )

    @classmethod
    def from_fen(cls, fen: str) -> "CastlingState":
        if fen == "-":
            return cls(False, False, False, False)
        return cls(
            white_kingside="K" in fen,
            white_queenside="Q" in fen,
            black_kingside="k" in fen,
            black_queenside="q" in fen,
        )


@dataclass
class PinnedPiece:
    piece: Piece
    pin_vector: tuple[int, int]
    pinning_piece_index: int
