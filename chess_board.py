from collections.abc import Iterator
from dataclasses import dataclass
import logging

from config import (
    FEN_CONVERSION,
    PieceMoves,
    CastlingState,
    WHITE,
    BLACK,
    EMPTY_SQUARE,
    PAWN,
    KNIGHT,
    BISHOP,
    ROOK,
    QUEEN,
    KING,
    WHITE_PAWN,
    WHITE_KNIGHT,
    WHITE_BISHOP,
    WHITE_ROOK,
    WHITE_QUEEN,
    WHITE_KING,
    BLACK_PAWN,
    BLACK_KNIGHT,
    BLACK_BISHOP,
    BLACK_ROOK,
    BLACK_QUEEN,
    BLACK_KING,
)

logger = logging.getLogger(__name__)

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
    EMPTY_SQUARE: ".",
    WHITE_PAWN: "P",
    BLACK_PAWN: "p",
    WHITE_KNIGHT: "N",
    BLACK_KNIGHT: "n",
    WHITE_BISHOP: "B",
    BLACK_BISHOP: "b",
    WHITE_ROOK: "R",
    BLACK_ROOK: "r",
    WHITE_QUEEN: "Q",
    BLACK_QUEEN: "q",
    WHITE_KING: "K",
    BLACK_KING: "k",
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
    board: list[int], skip_validation: bool = False
) -> tuple[list[int], list[int], list[int], list[int], int, int]:
    """ """
    w_pieces: list[int] = []
    w_idx: list[int] = []
    b_pieces: list[int] = []
    b_idx: list[int] = []
    w_king_idx = -1
    b_king_idx = -1

    for square_idx, piece in enumerate(board):
        if piece > 0:
            if piece == WHITE_KING:
                w_king_idx = square_idx
            w_pieces.append(piece)
            w_idx.append(square_idx)

        elif piece < 0:
            if piece == BLACK_KING:
                b_king_idx = square_idx
            b_pieces.append(piece)
            b_idx.append(square_idx)

    if not skip_validation and (w_king_idx == -1 or b_king_idx == -1):
        raise ValueError("A king is missing from the board")

    return (
        w_pieces,
        w_idx,
        b_pieces,
        b_idx,
        w_king_idx,
        b_king_idx,
    )


def parse_fen_to_board(fen: str) -> list[int]:
    """ """
    import re

    pattern = r"^([1-8pPrRnNbBqQkK/]+) ([wb]) ([KQkq-]+) ([a-h][1-8]|-) (\d+) (\d+)$"
    matches = re.match(pattern, fen)

    if matches is None:
        raise ValueError("Wrong fen string input")

    for match in matches.groups():
        print(match)

    board_match, active_color, castling, en_passant, half_moves, full_moves = (
        matches.groups()
    )

    ranks = board_match.split("/")

    board: list[int] = []

    for rank in ranks[::-1]:
        for c in rank:
            if c.isdigit():
                board.extend([EMPTY_SQUARE] * int(c))
            else:
                board.append(FEN_CONVERSION[c])

    return board


def parse_fen_to_chess_game(fen: str): ...


@dataclass
class BoardState:
    w_pieces: list[int]
    w_idx: list[int]
    b_pieces: list[int]
    b_idx: list[int]
    w_king_idx: int
    b_king_idx: int

    @classmethod
    def from_board(cls, board: list[int]) -> "BoardState":
        piece_data = find_pieces(board)
        return cls(
            w_pieces=piece_data[0],
            w_idx=piece_data[1],
            b_pieces=piece_data[2],
            b_idx=piece_data[3],
            w_king_idx=piece_data[4],
            b_king_idx=piece_data[5],
        )

    def get_color_state(self, color: int) -> tuple[list[int], list[int], int]:
        if color == WHITE:
            return (self.w_pieces, self.w_idx, self.w_king_idx)
        else:
            return (self.b_pieces, self.b_idx, self.b_king_idx)


@dataclass
class Square:
    square: str | int

    def __init__(self, square: str | int):
        if isinstance(square, str):
            return square_to_index(square)
        else:
            return square


class ChessBoard:
    def __init__(self, starting_position: bool = False):
        self.board: list[int] = (
            create_starting_position() if starting_position else create_empty_board()
        )
        self._update_board_state()

    def _square_to_index(self, square: str | int) -> int:
        if isinstance(square, int):
            return square
        return square_to_index(square)

    def _update_board_state(self) -> None:
        piece_data = find_pieces(self.board, skip_validation=True)
        self.w_pieces: list[int] = piece_data[0]
        self.w_idx: list[int] = piece_data[1]
        self.b_pieces: list[int] = piece_data[2]
        self.b_idx: list[int] = piece_data[3]
        self.w_king_idx: int = piece_data[4]
        self.b_king_idx: int = piece_data[5]

    def __getitem__(self, key: str | int) -> int:
        return self.board[self._square_to_index(key)]

    def __setitem__(self, key: str | int, value: int) -> None:
        self.board[self._square_to_index(key)] = value
        self._update_board_state()

    def __iter__(self) -> Iterator[int]:
        return iter(self.board)

    def __len__(self) -> int:
        return 64

    def make_move(self, from_square: str | int, to_square: str | int) -> None:
        idx1 = self._square_to_index(from_square)
        idx2 = self._square_to_index(to_square)

        if self.board[idx1] == EMPTY_SQUARE:
            raise ValueError("Trying to make a move on an EMPTY_SQUARE")

        self.board[idx2] = self.board[idx1]
        self.board[idx1] = EMPTY_SQUARE

        self._update_board_state()

    def display(self) -> None:
        display_board(self.board)

    def display_attributes(self) -> None:
        print(f"board={self.board}")
        print(f"w_pieces={self.w_pieces}")
        print(f"w_idx={self.w_idx}")
        print(f"b_pieces={self.b_pieces}")
        print(f"b_idx={self.b_idx}")
        print(f"w_king_idx={self.w_king_idx}")
        print(f"b_king_idx={self.b_king_idx}")

    def copy(self) -> "ChessBoard":
        """Create a copy of the board"""
        new_board = ChessBoard()
        new_board.board = self.board.copy()
        new_board._update_board_state()
        return new_board

    @classmethod
    def from_fen(cls, fen: str) -> "ChessBoard":
        board = ChessBoard()
        board.board = parse_fen_to_board(fen)
        board._update_board_state()
        return board

    @classmethod
    def setup_position(cls, piece_dict: dict[str, int]):
        board = ChessBoard()
        for square, piece in piece_dict.items():
            board[square] = piece

        return board


if __name__ == "__main__":
    b = ChessBoard.setup_position({"a1": WHITE_BISHOP, "e5": BLACK_KING})

    b.display()
