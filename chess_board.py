import logging

logger = logging.getLogger(__name__)

EMPTY_SQUARE = 0
WHITE_PAWN, BLACK_PAWN = 1, -1
WHITE_KNIGHT, BLACK_KNIGHT = 2, -2
WHITE_BISHOP, BLACK_BISHOP = 3, -3
WHITE_ROOK, BLACK_ROOK = 4, -4
WHITE_QUEEN, BLACK_QUEEN = 5, -5
WHITE_KING, BLACK_KING = 6, -6

PIECE_SYMBOLS = {
    EMPTY_SQUARE: "·",
    WHITE_PAWN: "♙",
    BLACK_PAWN: "♟",
    WHITE_KNIGHT: "♘",
    BLACK_KNIGHT: "♞",
    WHITE_BISHOP: "♗",
    BLACK_BISHOP: "♝",
    WHITE_ROOK: "♖",
    BLACK_ROOK: "♜",
    WHITE_QUEEN: "♕",
    BLACK_QUEEN: "♛",
    WHITE_KING: "♔",
    BLACK_KING: "♚",
}

PIECE_NAMES = {
    0: ".",
    1: "P",
    -1: "p",
    2: "N",
    -2: "n",
    3: "B",
    -3: "b",
    4: "R",
    -4: "r",
    5: "Q",
    -5: "q",
    6: "K",
    -6: "k",
}


def create_empty_board():
    return [0] * 64


def create_starting_position() -> list[int]:
    "Return the sarting position of a chess game as an array."
    board = [0] * 64

    board[0:8] = [
        WHITE_ROOK,
        WHITE_KNIGHT,
        WHITE_BISHOP,
        WHITE_QUEEN,
        WHITE_KING,
        WHITE_BISHOP,
        WHITE_KNIGHT,
        WHITE_ROOK,
    ]

    board[8:16] = [WHITE_PAWN] * 8

    board[48:56] = [BLACK_PAWN] * 8

    board[56:64] = [
        BLACK_ROOK,
        BLACK_KNIGHT,
        BLACK_BISHOP,
        BLACK_QUEEN,
        BLACK_KING,
        BLACK_BISHOP,
        BLACK_KNIGHT,
        BLACK_ROOK,
    ]

    return board


def display_board(board: list[int]) -> None:
    """
    Display a chess board with pieces as numbers in the terminal.
    """
    print("    a b c d e f g h")
    print("    ---------------")
    for rank in range(7, -1, -1):
        print(f"{rank + 1} | ", end="")
        for file in range(8):
            square = rank * 8 + file
            print(f"{PIECE_NAMES[board[square]]} ", end="")
        print(f"| {rank + 1}")
    print("    ---------------")
    print("    a b c d e f g h")


def pretty_display_board(board: list[int]) -> None:
    """
    Display a 'pretty' chess board with ASCI pieces.
    """
    print("   a b c d e f g h")
    print("   ----------------")
    for rank in range(8, 0, -1):
        row = board[(rank - 1) * 8 : rank * 8]
        symbols = [PIECE_SYMBOLS[p] for p in row]
        print(f"{rank} |{' '.join(symbols)} | {rank}")

    print("   ----------------")
    print("   a b c d e f g h")


def parse_color(board: list[int], square: str) -> str:
    piece = board[square_to_index(square)]
    if piece == 0:
        raise ValueError(f"Square '{square}' is not a piece.")
    return "w" if piece > 0 else "b"


def parse_square(square: str) -> tuple[int, int]:
    """Parse a classical chess square 'a1' into two int (file, rank)"""
    return ord(square[0]) - 96, int(square[1])


def parse_coordinates(file: int, rank: int) -> str:
    """
    Parse coordinates back into a chess square eg. 'a1' for (1, 1)
    """
    return f"{chr(file + 96)}{rank}"


def is_rook_aligned(sqr1: str, sqr2: str) -> bool:
    """Check if two pieces are rook aligned, meaning on the same row or rank"""
    f1, r1 = parse_square(sqr1)
    f2, r2 = parse_square(sqr2)
    return (f1 == f2) or (r1 == r2)


def is_on_same_diagonal(sqr1: str, sqr2: str) -> bool:
    """Check if two pieces are on the same diagonal"""
    f1, r1 = parse_square(sqr1)
    f2, r2 = parse_square(sqr2)
    return abs(f1 - r1) == abs(f2 - r2)


def square_to_index(square: str, skip_validation: bool = False) -> int:
    """
    Turn a 2 chr square into an index for a `board` list (from 0 to 63).
    """
    if not skip_validation:
        validate_square(square)

    f, r = parse_square(square)

    return (r - 1) * 8 + f - 1


def index_to_square(index: int) -> str:
    """
    Turn a `board` index into a chess square with two characters.
    """
    if not 0 <= index < 64:
        raise ValueError("Index must be an integer between '0' and '64'")

    rank = index // 8
    file = chr((index % 8) + 97)

    return f"{file}{rank + 1}"


def validate_square(square: str) -> None:
    """
    Validate that a 2 char string is part of a chess board.

    Raises:
        ValueError
            - not 2 chr
            - first chr is a letter a -> h
            - second chr is a number 1 -> 8
    """
    if len(square) != 2:
        raise ValueError("Wrong square input")

    if square[0] not in ["a", "b", "c", "d", "e", "f", "g", "h"]:
        raise ValueError("First symbol must be a letter between 'a' and 'h'")

    if not 0 < int(square[1]) < 9:
        raise ValueError("Rank must be a number from 1 to 8")


if __name__ == "__main__":
    board = create_starting_position()

    print(is_on_same_diagonal("a1", "h8"))
    print(is_on_same_diagonal("a1", "f8"))
    print(is_rook_aligned("e4", "h8"))
    print(is_rook_aligned("e4", "e8"))
