from dataclasses import dataclass
from time import time
from config import (
    Move,
    Piece,
    PieceMoves,
    WHITE,
    BLACK,
    PAWN,
    QUEEN,
    ROOK,
    BISHOP,
    KNIGHT,
)
from game_state import GameState
from legal_moves import generate_legal_moves

PROMOTION_LIST = [QUEEN, ROOK, BISHOP, KNIGHT]


def simple_selection(
    game_state: GameState, piece_moves: PieceMoves
) -> tuple[Piece, int, int | None]:
    color = game_state.active_color
    if color == WHITE:
        best_eval = float("-inf")
        promotion_rank = [i for i in range(56, 64, 1)]
    else:
        best_eval = float("+inf")
        promotion_rank = [i for i in range(0, 8, 1)]

    for piece, move in zip(piece_moves.pieces, piece_moves.move_list):
        for square in move:
            if (abs(piece.piece) == PAWN) and (square in promotion_rank):
                for promotion in PROMOTION_LIST:
                    g = game_state.copy()
                    g.make_move(piece, square, promotion)
                    eval = g.evaluate()
                    if color == WHITE and eval > best_eval:
                        best_move = (piece, square, promotion)
                        best_eval = eval
                    elif color == BLACK and eval < best_eval:
                        best_move = (piece, square, promotion)
                        best_eval = eval

            else:
                g = game_state.copy()
                g.make_move(piece, square)
                eval = g.evaluate()
                if color == WHITE and eval > best_eval:
                    best_move = (piece, square, None)
                    best_eval = eval
                elif color == BLACK and eval < best_eval:
                    best_move = (piece, square, None)
                    best_eval = eval

    return best_move  # pyright: ignore[reportPossiblyUnboundVariable]


def min_max(
    game_state: GameState,
    depth: int,
    maximazing: bool,
    alpha: float = -5000,
    beta: float = 5000,
) -> float:
    promotion_rank = (
        [i for i in range(56, 64, 1)]
        if game_state.active_color == WHITE
        else [i for i in range(0, 8, 1)]
    )
    if depth == 0 or game_state.draw or game_state.checkmate:
        return game_state.evaluate()
    if maximazing:
        best_eval = float("-inf")
        for piece, moves in zip(
            game_state.legal_moves.pieces, game_state.legal_moves.move_list
        ):
            for idx in moves:
                if (abs(piece.piece) == PAWN) and (idx in promotion_rank):
                    for promotion in PROMOTION_LIST:
                        g = game_state.copy()
                        g.make_move(piece, idx, promotion)
                        eval = min_max(g, depth - 1, False, alpha, beta)
                        best_eval = max(best_eval, eval)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            return best_eval
                else:
                    g = game_state.copy()
                    g.make_move(piece, idx)
                    eval = min_max(g, depth - 1, False, alpha, beta)
                    best_eval = max(best_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        return best_eval
        return best_eval
    else:
        best_eval = float("+inf")
        for piece, moves in zip(
            game_state.legal_moves.pieces, game_state.legal_moves.move_list
        ):
            for idx in moves:
                if (abs(piece.piece) == PAWN) and (idx in promotion_rank):
                    for promotion in PROMOTION_LIST:
                        g = game_state.copy()
                        g.make_move(piece, idx, promotion)
                        eval = min_max(g, depth - 1, True, alpha, beta)
                        best_eval = min(best_eval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            return best_eval
                else:
                    g = game_state.copy()
                    g.make_move(piece, idx)
                    eval = min_max(g, depth - 1, True, alpha, beta)
                    best_eval = min(best_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        return best_eval
        return best_eval


def minmax_selection(game_state: GameState, depth: int = 3) -> Move:
    start = time()
    piece_list = game_state.legal_moves.pieces
    moves_list = game_state.legal_moves.move_list

    if game_state.active_color == WHITE:
        best_eval = float("-inf")
        promotion_rank = [i for i in range(56, 64, 1)]

        for piece, move in zip(piece_list, moves_list):
            for square in move:
                if (abs(piece.piece) == PAWN) and (square in promotion_rank):
                    for promotion in PROMOTION_LIST:
                        g = game_state.copy()
                        g.make_move(piece, square, promotion)
                        eval = min_max(g, depth, False)
                        if eval > best_eval:
                            best_eval = eval
                            best_move = Move(piece, square)
                else:
                    g = game_state.copy()
                    g.make_move(piece, square)
                    eval = min_max(g, depth, False)
                    if eval > best_eval:
                        best_eval = eval
                        best_move = Move(piece, square)
    else:
        best_eval = float("+inf")
        promotion_rank = [i for i in range(0, 8, 1)]

        for piece, move in zip(piece_list, moves_list):
            for square in move:
                if (abs(piece.piece) == PAWN) and (square in promotion_rank):
                    for promotion in PROMOTION_LIST:
                        g = game_state.copy()
                        g.make_move(piece, square, promotion)
                        eval = min_max(g, depth, True)
                        if eval < best_eval:
                            best_eval = eval
                            best_move = Move(piece, square)
                else:
                    g = game_state.copy()
                    g.make_move(piece, square)
                    eval = min_max(g, depth, True)
                    if eval < best_eval:
                        best_eval = eval
                        best_move = Move(piece, square)

    end = time()
    duration = end - start
    print(f"duration: {duration}")

    return best_move
