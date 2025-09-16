import config
import logging

logger = logging.getLogger(__name__)

PIECE_SYMBOLS = {
    config.EMPTY_SQUARE: "·",
    config.WHITE_PAWN: "♙",
    config.BLACK_PAWN: "♟",
    config.WHITE_KNIGHT: "♘",
    config.BLACK_KNIGHT: "♞",
    config.WHITE_BISHOP: "♗",
    config.BLACK_BISHOP: "♝",
    config.WHITE_ROOK: "♖",
    config.BLACK_ROOK: "♜",
    config.WHITE_QUEEN: "♕",
    config.BLACK_QUEEN: "♛",
    config.WHITE_KING: "♔",
    config.BLACK_KING: "♚",
}

PIECE_NAMES = {
    config.EMPTY_SQUARE: ".",
    config.WHITE_PAWN: "P",
    config.BLACK_PAWN: "p",
    config.WHITE_KNIGHT: "N",
    config.BLACK_KNIGHT: "n",
    config.WHITE_BISHOP: "B",
    config.BLACK_BISHOP: "b",
    config.WHITE_ROOK: "R",
    config.BLACK_ROOK: "r",
    config.WHITE_QUEEN: "Q",
    config.BLACK_QUEEN: "q",
    config.WHITE_KING: "K",
    config.BLACK_KING: "k",
}


def create_empty_board():
    return [0] * 64


def create_starting_position() -> list[int]:
    "Return the sarting position of a chess game as an array."
    board = [0] * 64

    board[0:8] = [
        config.WHITE_ROOK,
        config.WHITE_KNIGHT,
        config.WHITE_BISHOP,
        config.WHITE_QUEEN,
        config.WHITE_KING,
        config.WHITE_BISHOP,
        config.WHITE_KNIGHT,
        config.WHITE_ROOK,
    ]

    board[8:16] = [config.WHITE_PAWN] * 8

    board[48:56] = [config.BLACK_PAWN] * 8

    board[56:64] = [
        config.BLACK_ROOK,
        config.BLACK_KNIGHT,
        config.BLACK_BISHOP,
        config.BLACK_QUEEN,
        config.BLACK_KING,
        config.BLACK_BISHOP,
        config.BLACK_KNIGHT,
        config.BLACK_ROOK,
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


def parse_square(square: str) -> tuple[int, int]:
    """
    Parse a classical chess square 'a1' into two int (file, rank).

    The returned coordinates range from 1 to 8 included.
    ex:
        - parse_square('a1') -> (1,1)
        - parse_square('h8') -> (8,8)
    """
    return ord(square[0]) - 96, int(square[1])


def parse_index(index: int) -> tuple[int, int]:
    """
    Parse the board: list[int] index into two ints (file, rank).

    The returned coordinates range from 1 to 8 included.
    ex:
        - parse_index(0) -> (1,1)
        - parse_index(63) -> (8,8)
    """
    file: int = index % 8 + 1
    rank: int = index // 8 + 1
    return file, rank


def parse_coordinates_to_idx(file: int, rank: int) -> int:
    """
    Parse coordinates back into the board index of those coordinates eg. 0 for (1, 1)
    """
    return (file - 1) + (rank - 1) * 8


def parse_coordinates_to_sqr(file: int, rank: int) -> str:
    """
    Parse coordinates back into a chess square eg. 'a1' for (1, 1)
    """
    return f"{chr(file + 96)}{rank}"


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


def is_square_aligned(sqr1: str, sqr2: str) -> bool:
    """Check if two pieces are rook aligned, meaning on the same row or rank using the chess square"""
    f1, r1 = parse_square(sqr1)
    f2, r2 = parse_square(sqr2)
    return (f1 == f2) or (r1 == r2)


def is_index_aligned(idx1: int, idx2: int) -> bool:
    """Check if two pieces are rook aligned, meaning on the same row or rank using the board: list[int] index"""
    f1, r1 = parse_index(idx1)
    f2, r2 = parse_index(idx2)
    return (f1 == f2) or (r1 == r2)


def is_square_on_diagonal(sqr1: str, sqr2: str) -> bool:
    """Check if two pieces are on the same diagonal using the chess square"""
    f1, r1 = parse_square(sqr1)
    f2, r2 = parse_square(sqr2)
    return abs(f1 - f2) == abs(r1 - r2)


def is_index_on_diagonal(idx1: int, idx2: int) -> bool:
    """Check if two pieces are on the same diagonal using the board: list[int] index"""
    f1, r1 = parse_index(idx1)
    f2, r2 = parse_index(idx2)
    return abs(f1 - f2) == abs(r1 - r2)


def find_pieces(
    board: list[int],
) -> config.BoardState:
    """ """
    w_pieces: list[int] = []
    w_idx: list[int] = []
    b_pieces: list[int] = []
    b_idx: list[int] = []
    w_king_idx = -1
    b_king_idx = -1

    for square_idx, piece in enumerate(board):
        if piece > 0:
            if piece == config.WHITE_KING:
                w_king_idx = square_idx
            w_pieces.append(piece)
            w_idx.append(square_idx)

        elif piece < 0:
            if piece == config.BLACK_KING:
                b_king_idx = square_idx
            b_pieces.append(piece)
            b_idx.append(square_idx)

    if w_king_idx == -1 or b_king_idx == -1:
        raise ValueError("A king is missing from the board")

    return (
        w_pieces,
        w_idx,
        b_pieces,
        b_idx,
        w_king_idx,
        b_king_idx,
    )


if __name__ == "__main__":
    board = create_starting_position()

    a = parse_index(0)
    print(a)
    b = parse_index(63)
    print(b)

    c = parse_coordinates_to_idx(1, 1)
    print(c)

    d = parse_coordinates_to_idx(8, 8)
    print(d)
