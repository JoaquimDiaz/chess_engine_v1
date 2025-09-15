import chess_board as cb
import move_generation as mv
import game_logic as gl
import config
import logging
from typing import Literal

logger = logging.getLogger(__name__)


def main():
    board = cb.create_starting_position()

    board = find_best_move(board, config.WHITE)


def generate_legal_moves(board: list[int], color: Literal[1, 0]) -> list[str]:
    # List of candidate move
    move_list: list[str] = []

    # Tuple with pieces position on the board
    board_state = cb.find_pieces(board)

    # 2 Lists with checking and pinned pieces in the position
    if color == config.WHITE:
        checking_pieces, pinned_pieces = gl.analyze_king_safety(board, board_state[4])
    elif color == config.BLACK:
        checking_pieces, pinned_pieces = gl.analyze_king_safety(board, board_state[5])

    if len(checking_pieces) > 1:
        return mv.generate_king_legal_moves(board, board_state, color)

    # Generating the list of all available moves ignoring legality
    move_list.extend(mv.generate_all_moves(board, board_state, pinned_pieces, color))

    if len(checking_pieces) == 1:
        move_list = filter_legal_moves(board, board_state, pinned_pieces, color)

    return move_list


def find_best_move(board: list[int], color: int) -> list[int]:
    best_move = evaluate_minmax(board, move_list, color)

    new_board = make_move(board, best_move)

    return new_board


if __name__ == "__main__":
    main()
