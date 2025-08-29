from chess_board import index_to_square, square_to_index, create_starting_position
import pytest

def test_sqr_idx_conversion():
    """Test that square conversion work for each square/index"""
    for i in range(64):
        
        square = index_to_square(i)
        
        assert square_to_index(square) == i
    
def test_invalid_squares():
    """Test that invalid square conversion raise a ValueError"""
    with pytest.raises(ValueError):
        square_to_index('z9')

    with pytest.raises(ValueError):
        index_to_square(64)
        
    with pytest.raises(ValueError):
        index_to_square(-12)

    with pytest.raises(ValueError):
        square_to_index('a9')

def test_starting_position():
    """Test that starting position is set up correctly"""
    board = create_starting_position()

    assert board[0] == 4   # White rook on a1
    assert board[4] == 6   # White king on e1  
    assert board[8] == 1   # White pawn on a2
    assert board[56] == -4 # Black rook on a8
    assert board[60] == -6 # Black king on e8