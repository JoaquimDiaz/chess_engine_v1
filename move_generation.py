from chess_board import create_starting_position, square_to_index, index_to_square

def generate_pawn_move(board, square):
    file = square[0]
    rank = int(square[1])
    
    piece = board[square_to_index(square)]
    if abs(piece) != 1:
        return []

    color = 'w' if piece > 0 else 'b'
     
    if (color == 'w' and rank == 8) or (color == 'b' and rank == 1):
        return []
    
    available_squares = []

    # ------ PAWN MOVES ------ #
    sqr1 = f"{file}{rank + 1}" if color == 'w' else f"{file}{rank - 1}"
    idx1 = square_to_index(sqr1)
    if board[idx1] == 0:
        available_squares.append(sqr1)

        if (color == 'w' and rank == 2) or (color == 'b' and rank == 7):
            sqr2 = f"{file}{rank + 2}" if color == 'w' else f"{file}{rank - 2}"
            idx2 = square_to_index(sqr2)
            if board[idx2] == 0:
                available_squares.append(sqr2)

    # ------ PAWN CAPTURES ------ #
    if color == 'w':
        capturable_squares = [f"{chr(ord(file) + 1)}{rank + 1}", f"{chr(ord(file) - 1)}{rank + 1}"]

    else:
        capturable_squares = [f"{chr(ord(file) + 1)}{rank - 1}", f"{chr(ord(file) - 1)}{rank - 1}"]


    return [(square, to_sqr) for to_sqr in available_squares]


if __name__ == "__main__":
    board = create_starting_position()
    
    pawn_moves_a2 = generate_pawn_move(board=board, square='a2')
    pawn_moves_e2 = generate_pawn_move(board=board, square='e2')
    pawn_moves_a7 = generate_pawn_move(board=board, square='a7')
    pawn_moves_f7 = generate_pawn_move(board=board, square='f7')
    pawn_moves_e1 = generate_pawn_move(board=board, square='e1')
    pawn_moves_e4 = generate_pawn_move(board=board, square='e4')

    print(f"'a2' -> {pawn_moves_a2}")
    print(f"'e2' -> {pawn_moves_e2}")
    print(f"'a7' -> {pawn_moves_a7}")
    print(f"'f7' -> {pawn_moves_f7}")
    print(f"'e1' -> {pawn_moves_e1}")
    print(f"'e4' -> {pawn_moves_e4}")
        
        