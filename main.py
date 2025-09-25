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
)
from legal_moves import generate_legal_moves
from game_state import GameState
from move_selection import simple_selection

logger = logging.getLogger(__name__)


def sq(square: str) -> int:
    return square_to_index(square)


def main():
    g = GameState.from_fen(
        "rnb1k1nr/pppp1ppp/5q2/2bNp3/4P3/8/PPPP1PPP/R1BQKBNR w KQkq - 4 4"
    )

    display_board(g.board)

    p = generate_legal_moves(g)
    piece, move = simple_selection(g, p)
    print(piece, move)

    display_board(g.board)

    g.make_move(piece, move)

    display_board(g.board)


if __name__ == "__main__":
    main()
