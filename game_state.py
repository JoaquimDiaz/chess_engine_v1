from typing import override
import chess_board as cb
import re

from chess_board import (
    BoardState,
    create_starting_position,
    index_to_square,
    display_board,
)
from game_logic import analyze_king_safety

from evaluate_position import evaluate_position

from config import (
    BLACK_ROOK,
    FEN_CONVERSION,
    BOARD_TO_FEN,
    EMPTY_SQUARE,
    KING,
    BLACK,
    PAWN,
    WHITE,
    ROOK,
    CastlingState,
    Piece,
    PieceMoves,
    WHITE_ROOK,
    PinnedPiece,
)
from legal_moves import generate_legal_moves

FEN_START = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

# ===============================================================
# GAMESTATE CLASS
# ===============================================================


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

        self.board_state: BoardState = BoardState.from_board(self.board)

        self._update_king_safety()
        self._update_legal_moves()
        self._update_endgame_state()

    @override
    def __str__(self):
        return f"""{{
        "board": {self.board},
        "active_color": {"WHITE" if self.active_color == WHITE else "BLACK"},
        "castling_state": {self.castling_state},
        "en_passant_target": {self.en_passant_target},
        "half_moves": {self.half_moves},
        "full_moves": {self.full_moves},
        "checkmate": {self.checkmate},
        "draw": {self.draw}
    }}"""

    def display(self) -> None:
        display_board(self.board)

    def copy(self) -> "GameState":
        return GameState(
            self.board.copy(),
            self.active_color,
            self.castling_state.copy(),
            self.en_passant_target,
            self.half_moves,
            self.full_moves,
        )

    def to_fen(self) -> str:
        return game_state_to_fen(self)

    # @property
    # def legal_moves(self) -> PieceMoves:
    #    return generate_legal_moves(
    #        self.board,
    #        self.active_color,
    #        self.board_state,
    #        self.checking_pieces,
    #        self.pinned_pieces,
    #        self.castling_state,
    #        self.en_passant_target,
    #    )

    # ---------------------------------------------------------------------
    # MAKING A MOVE
    # ---------------------------------------------------------------------

    def make_move(self, piece: Piece, move: int, promotion: int | None = None) -> None:
        self._update_half_moves(piece, move)
        self._update_board(piece, move, promotion)
        self._update_castling_state(piece)
        self._update_en_passant_target(piece, move)

        if self.active_color == BLACK:
            self.full_moves += 1

        self._update_board_state()

        self.active_color = WHITE if self.active_color == BLACK else BLACK

        self._update_king_safety()
        self._update_legal_moves()
        self._update_endgame_state()

    def _update_board(
        self, piece: Piece, move: int, promotion: int | None = None
    ) -> None:
        # Special moves?
        ## PAWN moving to last rank -> promotion
        if promotion is not None:
            self.board[piece.index] = EMPTY_SQUARE
            self.board[move] = promotion

        ## Castling Kingside
        elif (
            abs(piece.piece) == KING
            and self.castling_state.can_castle_kingside(self.active_color)
            and move in [62, 6]
        ):
            ### Mutate KING
            self.board[piece.index] = EMPTY_SQUARE
            self.board[move] = piece.piece

            ### Mutate ROOK
            from_idx = 7 if self.active_color == WHITE else 63
            to_idx = 5 if self.active_color == WHITE else 61
            self.board[from_idx] = EMPTY_SQUARE
            self.board[to_idx] = (
                WHITE_ROOK if self.active_color == WHITE else BLACK_ROOK
            )

        ## Castling Queenside
        elif (
            abs(piece.piece) == KING
            and self.castling_state.can_castle_queenside(self.active_color)
            and move in [58, 2]
        ):
            ### Mutate KING
            self.board[piece.index] = EMPTY_SQUARE
            self.board[move] = piece.piece

            ### Mutate ROOK
            from_idx = 0 if self.active_color == WHITE else 56
            to_idx = 3 if self.active_color == WHITE else 59
            self.board[from_idx] = EMPTY_SQUARE
            self.board[to_idx] = (
                WHITE_ROOK if self.active_color == WHITE else BLACK_ROOK
            )
        # Not a special move? mutate
        else:
            self.board[piece.index] = EMPTY_SQUARE
            self.board[move] = piece.piece

    def _update_castling_state(self, piece: Piece) -> None:
        if piece.piece == abs(KING):
            self.castling_state.disable_all(self.active_color)
        elif abs(piece.piece) == ROOK and piece.index in [7, 63]:
            self.castling_state.disable_kingside(self.active_color)
        elif abs(piece.piece) == ROOK and piece.index in [0, 56]:
            self.castling_state.disable_queenside(self.active_color)

    def _update_en_passant_target(self, piece: Piece, move: int):
        if abs(piece.piece) == PAWN and abs(piece.index - move) == 16:
            self.en_passant_target = (
                piece.index + 8 if self.active_color == WHITE else piece.index - 8
            )

    def _update_half_moves(self, piece: Piece, move: int) -> None:
        if abs(piece.piece) == PAWN or self.board[move] != EMPTY_SQUARE:
            self.half_moves = 0
        else:
            self.half_moves += 1

    def _update_board_state(self) -> None:
        self.board_state = BoardState.from_board(self.board)

    def _update_king_safety(self) -> None:
        active_king_idx = (
            self.board_state.w_king_idx
            if self.active_color == WHITE
            else self.board_state.b_king_idx
        )

        safety = analyze_king_safety(self.board, active_king_idx, self.active_color)

        self.checking_pieces: list[Piece] = safety[0]
        self.pinned_pieces: list[PinnedPiece] = safety[1]

    def _update_legal_moves(self):
        self.legal_moves: PieceMoves = generate_legal_moves(
            self.board,
            self.active_color,
            self.board_state,
            self.checking_pieces,
            self.pinned_pieces,
            self.castling_state,
            self.en_passant_target,
        )

    def _update_endgame_state(self) -> None:
        if not self.legal_moves:
            if self.checking_pieces != []:
                self.checkmate: bool = True
            else:
                self.draw: bool = True
        elif self.half_moves == 100:
            self.draw = True
        else:
            self.checkmate = False
            self.draw = False

    # ---------------------------------------------------------------------
    # POSITION EVALUATION
    # ---------------------------------------------------------------------

    def evaluate(self) -> float:
        return evaluate_position(
            self.active_color,
            self.board_state.w_pieces,
            self.board_state.b_pieces,
            self.checkmate,
            self.draw,
        )

    # ---------------------------------------------------------------------
    # CLASS METHOD
    # ---------------------------------------------------------------------

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


# ===============================================================
# FEN PARSING UTILS
# ===============================================================


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
