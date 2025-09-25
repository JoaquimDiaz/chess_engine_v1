from game_state import GameState
import move_generation as mv
import game_logic as gl
import logging

from chess_board import ChessBoard, BoardState, create_starting_position
from config import BLACK, WHITE, CastlingState, Piece, PieceMoves

logger = logging.getLogger(__name__)


def find_best_move(game_state: GameState, piece_moves: PieceMoves) -> tuple[Piece, int]:
    piece_moves = generate_legal_moves(
        game_state.board,
        game_state.active_color,
        game_state.board_state,
        game_state.castling_state,
        game_state.en_passant_target,
    )

    best_move = evaluate_moves(game_state, piece_moves)

    return best_move
