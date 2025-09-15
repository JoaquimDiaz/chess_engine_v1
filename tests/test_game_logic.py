import pytest
from move_generation import find_piece
from chess_board import (
    create_starting_position,
    create_empty_board,
    is_on_same_diagonal,
    is_rook_aligned,
)

empty_board = create_empty_board()
starting_position = create_starting_position()


def test_empty_position():
    """Test that an empty position returns no pieces"""
    assert find_pieces(empty_board, "w") == []
    assert find_pieces(empty_board, "b") == []


def test_starting_position():
    """Test that the starting position as 16 pieces for both colors"""
    assert len(find_pieces(starting_position, "w")) == 16
    assert len(find_pieces(starting_position, "b")) == 16


def test_color_separation():
    """Test that list contains only the corresponding color"""
    pieces_white = find_pieces(starting_position, "w")
    pieces_black = find_pieces(starting_position, "b")

    # verify all white pieces are positive values
    for piece, square in pieces_white:
        assert piece > 0

    # verify all black pieces are negative values
    for piece, square in pieces_black:
        assert piece < 0
