import logging

from chess_board import (
    ChessBoard,
    BoardState,
    create_starting_position,
    display_board,
    square_to_index,
)
from config import (
    BLACK,
    WHITE,
    WHITE_KING,
    WHITE_PAWN,
    CastlingState,
    Piece,
    PieceMoves,
    BLACK_KING,
    WHITE_ROOK,
)
from legal_moves import generate_legal_moves
from game_state import GameState
from move_selection import simple_selection, minmax_selection

logger = logging.getLogger(__name__)


def sq(square: str) -> int:
    return square_to_index(square)


def find(p: int, game_state: GameState) -> None:
    for piece, moves in zip(
        game_state.legal_moves.pieces, game_state.legal_moves.move_list
    ):
        if piece.piece == p:
            print(f"{piece}: {moves}")


def main():
    g = GameState.from_fen(
        "rnb1kbnr/pppp1ppp/8/4p3/2B1P2q/5QP1/PPPP1P1P/RNB1KN1R w KQkq - 0 1"
    )

    print(g)
    g.display()
    p = minmax_selection(g, 4)
    print(p)


if __name__ == "__main__":
    main()
