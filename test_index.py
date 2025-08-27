from chess_board import index_to_square, square_to_index

for i in range(64):
    
    square = index_to_square(i)
    
    assert square_to_index(square) == i