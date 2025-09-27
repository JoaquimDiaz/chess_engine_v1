import logging

from chess_board import (
    ChessBoard,
    BoardState,
    create_starting_position,
    display_board,
    index_to_square,
    square_to_index,
)
from config import (
    BLACK,
    WHITE,
    WHITE_KING,
    WHITE_PAWN,
    WHITE_QUEEN,
    CastlingState,
    Piece,
    PieceMoves,
    BLACK_KING,
    WHITE_ROOK,
    Move,
)
from legal_moves import generate_legal_moves
from game_state import GameState
from move_selection import simple_selection, minmax_selection, min_max

from benchmarks.profiler import profile_engine

logger = logging.getLogger(__name__)


fen_fried_live = "r1bqkb1r/pppp1ppp/2n2n2/4p1N1/2B1P3/8/PPPP1PPP/RNBQK2R b KQkq - 0 1"

fen_tactic_4 = "2r2kr1/R4p1p/4p3/1pqnPp2/5P2/Q7/P3N1PP/1R5K w - - 1 2"


def sq(square: str) -> int:
    return square_to_index(square)


def find(p: int, game_state: GameState) -> None:
    for piece, moves in zip(
        game_state.legal_moves.pieces, game_state.legal_moves.move_list
    ):
        if piece.piece == p:
            print(f"{piece}: {moves}")


def print_move(m: Move) -> None:
    print(
        f'{m.piece.piece} from "{index_to_square(m.piece.index)}" to "{index_to_square(m.to_idx)}'
    )


def main():
    start()


def start():
    g = GameState.from_fen(
        "r1bqkb1r/pppp1ppp/2n2n2/4p1N1/2B1P3/8/PPPP1PPP/RNBQK2R b KQkq - 0 1"
    )
    g.display()
    p = minmax_selection(g, 3)
    print_move(p)


def profile():
    fen = "2r2kr1/R4p1p/4p3/1pqnPp2/5P2/Q7/P3N1PP/1R5K w - - 1 2"
    move = profile_engine(fen, 3)

    print(move)


if __name__ == "__main__":
    main()
