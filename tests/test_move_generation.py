import chess_board as cb
import move_generation as mv
import toto
import pytest
import config

board = cb.create_empty_board()

board[cb.square_to_index("a2")] = config.BLACK_BISHOP
board[cb.square_to_index("d5")] = config.WHITE_KING


def test_generate_king_legal_moves():
    board_state = toto.find_pieces(board)
    king_legal_moves = mv.generate_king_legal_moves(board, board_state, config.WHITE)

    assert set(king_legal_moves) == set(["d6", "c6", "c5", "d4", "e5", "e4"])
