import chess_board as cb
from chess_board import ChessBoard, create_empty_board, create_starting_position
import pytest

from config import WHITE_KING, BLACK_KING


def test_create_empty_board():
    """Tests that the empty board is setup correctly"""
    board = create_empty_board()

    assert len(board) == 64
    assert sum(board) == 0


def test_create_starting_position():
    """Test that starting position is set up correctly"""
    board = cb.create_starting_position()

    assert board[0] == 4  # White rook on a1
    assert board[4] == 6  # White king on e1
    assert board[8] == 1  # White pawn on a2
    assert board[56] == -4  # Black rook on a8
    assert board[60] == -6  # Black king on e8


def test_parse_square():
    """ """
    assert cb.parse_square("a1") == (1, 1)
    assert cb.parse_square("h8") == (8, 8)
    assert cb.parse_square("d4") == (4, 4)
    assert cb.parse_square("a8") == (1, 8)
    assert cb.parse_square("h1") == (8, 1)


def test_sqr_coord_conversion():
    """Test that square/coordinate conversion works for each square/coordinates"""
    for x in range(1, 8, 1):
        for y in range(1, 8, 1):
            square = cb.parse_coordinates_to_sqr(x, y)

            assert cb.parse_square(square) == (x, y)


def test_parse_index():
    """ """
    assert cb.parse_index(0) == (1, 1)
    assert cb.parse_index(63) == (8, 8)
    assert cb.parse_index(27) == (4, 4)
    assert cb.parse_index(56) == (1, 8)
    assert cb.parse_index(7) == (8, 1)


def test_idx_coord_conversion():
    """ """
    for i in range(64):
        file, rank = cb.parse_index(i)

        assert i == cb.parse_coordinates_to_idx(file, rank)


def test_sqr_idx_conversion():
    """Test that square conversion work for each square/index"""
    for i in range(64):
        square = cb.index_to_square(i)

        assert cb.square_to_index(square) == i


def test_invalid_squares():
    """Test that invalid square conversion raise a ValueError"""
    with pytest.raises(ValueError):
        _ = cb.square_to_index("z9")

    with pytest.raises(ValueError):
        _ = cb.index_to_square(64)

    with pytest.raises(ValueError):
        _ = cb.index_to_square(-12)

    with pytest.raises(ValueError):
        _ = cb.square_to_index("a9")


def test_is_square_aligned():
    """ """
    assert cb.is_square_aligned("a1", "a7") == True
    assert cb.is_square_aligned("e4", "b4") == True
    assert cb.is_square_aligned("b5", "c4") == False


def test_is_square_on_diagonal():
    """ """
    assert cb.is_square_on_diagonal("a1", "h8") == True
    assert cb.is_square_on_diagonal("f4", "g5") == True
    assert cb.is_square_on_diagonal("a7", "g5") == False
    assert cb.is_square_on_diagonal("g3", "b8") == True


def test_is_index_aligned():
    """ """
    assert cb.is_index_aligned(3, 59) == True
    assert cb.is_index_aligned(24, 31) == True
    assert cb.is_index_aligned(57, 55) == False


def test_is_index_on_diagonal():
    """ """
    assert cb.is_index_on_diagonal(0, 63) == True
    assert cb.is_index_on_diagonal(22, 57) == True
    assert cb.is_index_on_diagonal(26, 37) == False


def test_find_pieces():
    """ """
    empty_board = cb.create_empty_board()

    with pytest.raises(ValueError):
        _ = cb.find_pieces(empty_board)

    board = cb.create_starting_position()
    board_state = cb.find_pieces(board)
    assert board_state[0] == [4, 2, 3, 5, 6, 3, 2, 4, 1, 1, 1, 1, 1, 1, 1, 1]
    assert board_state[1] == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

    assert board_state[2] == [
        -1,
        -1,
        -1,
        -1,
        -1,
        -1,
        -1,
        -1,
        -4,
        -2,
        -3,
        -5,
        -6,
        -3,
        -2,
        -4,
    ]
    assert board_state[3] == [i for i in range(48, 64, 1)]


def test_ChessBoard():
    b1 = ChessBoard()
    b2 = create_empty_board()

    b3 = ChessBoard(starting_position=True)
    b4 = create_starting_position()

    assert b1.board == b2
    assert b3.board == b4

    with pytest.raises(ValueError):
        b1["z8"] = WHITE_KING


def test_fen_to_board():
    fen_starting_board = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    b1 = cb.parse_fen_to_board(fen_starting_board)
    b2 = ChessBoard(True)

    assert b1 == b2.board
