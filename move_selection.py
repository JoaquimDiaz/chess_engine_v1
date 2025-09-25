from config import Piece, PieceMoves, WHITE, BLACK
from game_state import GameState
from legal_moves import generate_legal_moves


def simple_selection(
    game_state: GameState, piece_moves: PieceMoves
) -> tuple[Piece, int]:
    if game_state.active_color == WHITE:
        best_eval = float("-inf")
        color = WHITE
    else:
        best_eval = float("+inf")
        color = BLACK

    for piece, move in zip(piece_moves.pieces, piece_moves.move_list):
        for square in move:
            g = game_state.copy()
            g.make_move(piece, square)
            eval = g.evaluate()
            if color == WHITE and eval > best_eval:
                best_move = (piece, square)
                best_eval = eval
            elif color == BLACK and eval < best_eval:
                best_move = (piece, square)
                best_eval = eval

    return best_move  # pyright: ignore[reportPossiblyUnboundVariable]
