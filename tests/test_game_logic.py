import chess_board as cb
import move_generation as mv
import game_logic as gl
import config
import pytest

test_board = cb.create_empty_board()

test_board[0] = config.BLACK_BISHOP
test_board[62] = config.BLACK_ROOK
test_board[6] = config.BLACK_ROOK
test_board[54] = config.WHITE_KING
test_board[5] = config.BLACK_KING


def test_diagonal_checks():
    board = test_board[:]
    board_state = cb.find_pieces(board)
    checking_piece, pinned_piece = gl.directional_check(
        board, board_state[4], config.WHITE, (-1, -1)
    )
    assert pinned_piece is None
    assert checking_piece is not None
    assert board[checking_piece[1]] == config.BLACK_BISHOP


def test_diagonal_pin():
    board = test_board[:]
    board[18] = config.WHITE_QUEEN
    board_state = cb.find_pieces(board)

    checking_piece, pinned_piece = gl.directional_check(
        board, board_state[4], config.WHITE, (-1, -1)
    )

    assert checking_piece is None
    assert pinned_piece is not None
    assert board[pinned_piece[1]] == config.WHITE_QUEEN


def test_aligned_checks():
    board = test_board[:]
    board_state = cb.find_pieces(board)
    checking_piece, pinned_piece = gl.directional_check(
        board, board_state[4], config.WHITE, (0, 1)
    )
    assert pinned_piece is None
    assert checking_piece is not None
    assert board[checking_piece[1]] == config.BLACK_ROOK

    checking_piece, pinned_piece = gl.directional_check(
        board, board_state[4], config.WHITE, (0, -1)
    )
    assert pinned_piece is None
    assert checking_piece is not None
    assert board[checking_piece[1]] == config.BLACK_ROOK


def test_aligned_pin():
    board = test_board[:]
    board[14] = config.WHITE_QUEEN
    board_state = cb.find_pieces(board)

    checking_piece, pinned_piece = gl.directional_check(
        board, board_state[4], config.WHITE, (0, -1)
    )

    assert checking_piece is None
    assert pinned_piece is not None
    assert board[pinned_piece[1]] == config.WHITE_QUEEN


def test_knight_check():
    board = cb.create_empty_board()
    board[2] = config.BLACK_KING
    board[8] = config.WHITE_KNIGHT
    board[63] = config.WHITE_KING
    board_state = cb.find_pieces(board)

    result = gl.knight_check(board, config.BLACK, board_state[5])

    assert result is not None
    assert result[0] == 2
    assert result[1] == 8


def test_analyze_king_safety():
    b = cb.create_empty_board()
    with pytest.raises(ValueError):
        gl.analyze_king_safety(b, 0, config.BLACK)

    b[0] = config.WHITE_KING
    b[7] = config.BLACK_KING
    b[63] = config.BLACK_BISHOP

    checking_pieces, pinned_pieces = gl.analyze_king_safety(b, 0, config.WHITE)

    assert pinned_pieces == []
    assert checking_pieces != []
    assert len(checking_pieces) == 1

    piece, idx = checking_pieces[0]
    assert piece == config.BLACK_BISHOP
    assert idx == 63
