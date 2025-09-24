from typing import override
import chess_board as cb
import re

from chess_board import (
    BoardState,
    create_starting_position,
    index_to_square,
)
from config import (
    FEN_CONVERSION,
    BOARD_TO_FEN,
    EMPTY_SQUARE,
    BLACK,
    WHITE,
    CastlingState,
)

FEN_START = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


#################################
# ------ GameState CLASS ------ #
#################################


class GameState:
    def __init__(
        self,
        board: list[int],
        active_color: int,
        castling_state: CastlingState,
        en_passant_target: int | None = None,
        half_moves: int = 0,
        full_moves: int = 1,
    ):
        self.board: list[int] = board
        self.active_color: int = active_color
        self.castling_state: CastlingState = castling_state
        self.en_passant_target: int | None = en_passant_target
        self.half_moves: int = half_moves
        self.full_moves: int = full_moves

        # Derived state
        self.board_state: BoardState = BoardState.from_board(self.board)

    @override
    def __str__(self):
        return f"""{{\
        "board": {self.board},
        "active_color": {self.active_color},
        "castling_state": {self.castling_state},
        "en_passant_target": {self.en_passant_target},
        "half_moves": {self.half_moves},
        "full_moves": {self.full_moves}
    }}"""

    def to_fen(self):
        return game_state_to_fen(self)

    @classmethod
    def starting_position(cls) -> "GameState":
        """Create a game in the standard starting position"""
        return cls(
            board=create_starting_position(),
            active_color=WHITE,
            castling_state=CastlingState(),
            en_passant_target=None,
            half_moves=0,
            full_moves=1,
        )

    @classmethod
    def from_fen(cls, fen: str) -> "GameState":
        """Create a game from FEN string"""
        board, active_color, castling, en_passant, half, full = parse_fen(fen)
        return cls(
            board=parse_board_fen(board),
            active_color=parse_color_fen(active_color),
            castling_state=CastlingState.from_fen(castling),
            en_passant_target=parse_en_passant_fen(en_passant),
            half_moves=int(half),
            full_moves=int(full),
        )

    @classmethod
    def empty_board(cls) -> "GameState":
        """Create a game with empty board (for testing)"""
        return cls(
            board=[0] * 64,
            active_color=WHITE,
            castling_state=CastlingState(),
        )


###################################
# ------ FEN PARSING UTILS ------ #
###################################


def parse_fen(fen: str):
    pattern = r"^([1-8RrNnBbQqKkPp/]+) ([wb]) ([KkQq-]+) ([a-h][1-8]|-) (\d+) (\d+)$"
    match = re.match(pattern, fen)

    if match is None:
        raise ValueError("Wrong fen input")

    return match.groups()


def parse_board_fen(fen: str) -> list[int]:
    ranks: list[str] = fen.split("/")
    board: list[int] = []
    for rank in ranks[::-1]:
        for c in rank:
            if c.isdigit():
                board.extend([EMPTY_SQUARE] * int(c))
            else:
                board.append(FEN_CONVERSION[c])
    return board


def parse_color_fen(fen: str) -> int:
    return WHITE if fen == "w" else BLACK


def parse_en_passant_fen(fen: str) -> int | None:
    if fen == "-":
        return None
    else:
        return cb.square_to_index(fen)


def game_state_to_fen(game_state: GameState) -> str:
    board: str = ""
    square_count: int = 0
    empty_count: int = 0
    for s in game_state.board:
        if s == EMPTY_SQUARE:
            empty_count += 1
            square_count += 1
        else:
            if empty_count > 0:
                board += str(empty_count)
                empty_count = 0
            board += BOARD_TO_FEN[s]
            square_count += 1
        if square_count == 8:
            if empty_count > 0:
                board += str(empty_count)
                empty_count = 0
            board += "/"
            square_count = 0

    board = board.rstrip("/")

    active_color: str = "w" if game_state.active_color == WHITE else "b"

    castling_state = game_state.castling_state.to_fen()

    en_passant = (
        index_to_square(game_state.en_passant_target)
        if game_state.en_passant_target
        else "-"
    )

    fen: str = f"{board} {active_color} {castling_state} {en_passant} {game_state.half_moves} {game_state.full_moves}"

    return fen


if __name__ == "__main__":
    g = GameState.from_fen(FEN_START)
    print(g)

    print(game_state_to_fen(g))
