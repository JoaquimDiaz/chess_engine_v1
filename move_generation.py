from chess_board import create_starting_position, square_to_index, index_to_square, create_empty_board

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

    # creating a list of available files
    c = ord(file)
    files = []

    if c != ord('h'):
        files.append(chr(c + 1))

    if c != ord('a'):
        files.append(chr(c - 1))
     
    # defining rank up or down from color
    rank_capture = rank + 1 if color == 'w' else rank -1

    capturable_squares = [f"{f}{rank_capture}" for f in files]

    # adding squares to availables squares if there is an ennemy piece
    for s in capturable_squares:
        board_square = board[square_to_index(s)]
        if (board_square < 0 and color == 'w') or (board_square > 0 and color == 'b'):
            available_squares.append(s)

    return [(square, to_sqr) for to_sqr in available_squares]

def generate_knight_move(board, square):
    file = square[0] 
    rank = int(square[1])
    c = ord(file)
    piece = board[square_to_index(square)]
    color = 'w' if piece > 0 else 'b'

    potential_squares = []
    available_squares = []

    if abs(piece) != 2:
        return []

    potential_squares.append(f"{chr(c + 1)}{rank + 2}")
    potential_squares.append(f"{chr(c - 1)}{rank + 2}")
    potential_squares.append(f"{chr(c + 1)}{rank - 2}")
    potential_squares.append(f"{chr(c - 1)}{rank - 2}")
    potential_squares.append(f"{chr(c + 2)}{rank + 1}")
    potential_squares.append(f"{chr(c - 2)}{rank + 1}")
    potential_squares.append(f"{chr(c + 2)}{rank - 1}")
    potential_squares.append(f"{chr(c - 2)}{rank - 1}")
    
    for s in potential_squares:
        try:
            idx = square_to_index(s)
            if color == 'w' and board[idx] <= 0:
                available_squares.append(s)
            if color == 'b' and board[idx] >= 0:
                available_squares.append(s)
        except (ValueError, IndexError):
            continue
    
    return [(square, to_sqr) for to_sqr in available_squares]

def generate_rook_move(board, square):
    file = square[0]
    rank = int(square[1])
    c = ord(file)
    piece = board[square_to_index(square)]

    if abs(piece) != 4:
        return []
    
    color = 'w' if piece > 0 else 'b'

    available_squares = []
    
    ## left
    i = 0
    while c + i > 97:
        i -= 1
        sqr = f"{chr(c + i)}{rank}"
        piece_on_sqr = board[square_to_index(sqr)]
        if piece_on_sqr == 0:
            available_squares.append(sqr)
        elif (piece_on_sqr < 0 and color == 'w') or (piece_on_sqr > 0 and color == 'b'):
            available_squares.append(sqr)
            break
        else:
            break
    ## right
    i = 0
    while c + i < 104:
        i += 1
        sqr = f"{chr(c + i)}{rank}"
        piece_on_sqr = board[square_to_index(sqr)]
        if piece_on_sqr == 0:
            available_squares.append(sqr)
        elif (piece_on_sqr < 0 and color == 'w') or (piece_on_sqr > 0 and color == 'b'):
            available_squares.append(sqr)
            break
        else:
            break
    
    ## up
    i = 0
    while rank + i < 8:
        i += 1
        sqr = f"{file}{rank + i}"
        piece_on_sqr = board[square_to_index(sqr)]
        if piece_on_sqr == 0:
            available_squares.append(sqr)
        elif (piece_on_sqr < 0 and color == 'w') or (piece_on_sqr > 0 and color == 'b'):
            available_squares.append(sqr)
            break
        else:
            break
    
    ## down
    i = 0
    while rank + i > 1:
        i -= 1
        sqr = f"{file}{rank + i}"
        piece_on_sqr = board[square_to_index(sqr)]
        if piece_on_sqr == 0:
            available_squares.append(sqr)
        elif (piece_on_sqr < 0 and color == 'w') or (piece_on_sqr > 0 and color == 'b'):
            available_squares.append(sqr)
            break
        else:
            break
    
    return [(square, to_sqr) for to_sqr in available_squares]

def generate_bishop_move(board, square):
    file = square[0]
    rank = int(square[1])
    c = ord(file)
    piece = board[square_to_index(square)]

    available_squares = []
    
    if abs(piece) != 3:
        return []

    color = 'w' if piece > 0 else 'b'
    
    # up-right
    x, y = 0, 0
    while c + x < 104 and rank + y < 8:
        x += 1
        y += 1    

        sqr = f"{chr(c + x)}{rank + y}"
        piece_on_sqr = board[square_to_index(sqr)]

        if piece_on_sqr == 0:
            available_squares.append(sqr)
           
        elif (piece_on_sqr < 0 and color == 'w') or (piece_on_sqr > 0 and color == 'b'):
            available_squares.append(sqr)
            break

        else:
            break
    
    # up-left
    x, y = 0, 0
    while c + x > 97 and rank + y < 8:
        x -= 1
        y += 1

        sqr = f"{chr(c + x)}{rank + y}"
        piece_on_sqr = board[square_to_index(sqr)]

        if piece_on_sqr == 0:
            available_squares.append(sqr)
           
        elif (piece_on_sqr < 0 and color == 'w') or (piece_on_sqr > 0 and color == 'b'):
            available_squares.append(sqr)
            break

        else:
            break
        
        
    # down-left
    x, y = 0, 0
    while c + x > 97 and rank + y > 1:
        x -= 1
        y -= 1
    
        sqr = f"{chr(c + x)}{rank + y}"
        piece_on_sqr = board[square_to_index(sqr)]

        if piece_on_sqr == 0:
            available_squares.append(sqr)
           
        elif (piece_on_sqr < 0 and color == 'w') or (piece_on_sqr > 0 and color == 'b'):
            available_squares.append(sqr)
            break

        else:
            break
    
    # down-right
    x, y = 0, 0
    while c + x < 104 and rank + y > 1:
        x += 1
        y -= 1
    
        sqr = f"{chr(c + x)}{rank + y}"
        piece_on_sqr = board[square_to_index(sqr)]

        if piece_on_sqr == 0:
            available_squares.append(sqr)
           
        elif (piece_on_sqr < 0 and color == 'w') or (piece_on_sqr > 0 and color == 'b'):
            available_squares.append(sqr)
            break

        else:
            break

    return [(square, to_sqr) for to_sqr in available_squares]

def generate_queen_move(board, square):
    file = square[0]
    rank = int(square[1])
    c = ord(file)
    piece = board[square_to_index(square)]

    if abs(piece) != 5:
        return []
    
    color = 'w' if piece > 0 else 'b'

    available_squares = []
    
    ## left
    i = 0
    while c + i > 97:
        i -= 1
        sqr = f"{chr(c + i)}{rank}"
        piece_on_sqr = board[square_to_index(sqr)]
        if piece_on_sqr == 0:
            available_squares.append(sqr)
        elif (piece_on_sqr < 0 and color == 'w') or (piece_on_sqr > 0 and color == 'b'):
            available_squares.append(sqr)
            break
        else:
            break
    ## right
    i = 0
    while c + i < 104:
        i += 1
        sqr = f"{chr(c + i)}{rank}"
        piece_on_sqr = board[square_to_index(sqr)]
        if piece_on_sqr == 0:
            available_squares.append(sqr)
        elif (piece_on_sqr < 0 and color == 'w') or (piece_on_sqr > 0 and color == 'b'):
            available_squares.append(sqr)
            break
        else:
            break
    
    ## up
    i = 0
    while rank + i < 8:
        i += 1
        sqr = f"{file}{rank + i}"
        piece_on_sqr = board[square_to_index(sqr)]
        if piece_on_sqr == 0:
            available_squares.append(sqr)
        elif (piece_on_sqr < 0 and color == 'w') or (piece_on_sqr > 0 and color == 'b'):
            available_squares.append(sqr)
            break
        else:
            break
    
    ## down
    i = 0
    while rank + i > 1:
        i -= 1
        sqr = f"{file}{rank + i}"
        piece_on_sqr = board[square_to_index(sqr)]
        if piece_on_sqr == 0:
            available_squares.append(sqr)
        elif (piece_on_sqr < 0 and color == 'w') or (piece_on_sqr > 0 and color == 'b'):
            available_squares.append(sqr)
            break
        else:
            break
    
    # up-right
    x, y = 0, 0
    while c + x < 104 and rank + y < 8:
        x += 1
        y += 1    

        sqr = f"{chr(c + x)}{rank + y}"
        piece_on_sqr = board[square_to_index(sqr)]

        if piece_on_sqr == 0:
            available_squares.append(sqr)
           
        elif (piece_on_sqr < 0 and color == 'w') or (piece_on_sqr > 0 and color == 'b'):
            available_squares.append(sqr)
            break

        else:
            break
    
    # up-left
    x, y = 0, 0
    while c + x > 97 and rank + y < 8:
        x -= 1
        y += 1

        sqr = f"{chr(c + x)}{rank + y}"
        piece_on_sqr = board[square_to_index(sqr)]

        if piece_on_sqr == 0:
            available_squares.append(sqr)
           
        elif (piece_on_sqr < 0 and color == 'w') or (piece_on_sqr > 0 and color == 'b'):
            available_squares.append(sqr)
            break

        else:
            break
        
        
    # down-left
    x, y = 0, 0
    while c + x > 97 and rank + y > 1:
        x -= 1
        y -= 1
    
        sqr = f"{chr(c + x)}{rank + y}"
        piece_on_sqr = board[square_to_index(sqr)]

        if piece_on_sqr == 0:
            available_squares.append(sqr)
           
        elif (piece_on_sqr < 0 and color == 'w') or (piece_on_sqr > 0 and color == 'b'):
            available_squares.append(sqr)
            break

        else:
            break
    
    # down-right
    x, y = 0, 0
    while c + x < 104 and rank + y > 1:
        x += 1
        y -= 1
    
        sqr = f"{chr(c + x)}{rank + y}"
        piece_on_sqr = board[square_to_index(sqr)]

        if piece_on_sqr == 0:
            available_squares.append(sqr)
           
        elif (piece_on_sqr < 0 and color == 'w') or (piece_on_sqr > 0 and color == 'b'):
            available_squares.append(sqr)
            break

        else:
            break

    return [(square, to_sqr) for to_sqr in available_squares]

def generate_bishop_move(board, square):
    file = square[0]
    rank = int(square[1])
    c = ord(file)
    piece = board[square_to_index(square)]

    available_squares = []
    
    if abs(piece) != 3:
        return []

    color = 'w' if piece > 0 else 'b'
    
    # up-right
    x, y = 0, 0
    while c + x < 104 and rank + y < 8:
        x += 1
        y += 1    

        sqr = f"{chr(c + x)}{rank + y}"
        piece_on_sqr = board[square_to_index(sqr)]

        if piece_on_sqr == 0:
            available_squares.append(sqr)
           
        elif (piece_on_sqr < 0 and color == 'w') or (piece_on_sqr > 0 and color == 'b'):
            available_squares.append(sqr)
            break

        else:
            break
    
    # up-left
    x, y = 0, 0
    while c + x > 97 and rank + y < 8:
        x -= 1
        y += 1

        sqr = f"{chr(c + x)}{rank + y}"
        piece_on_sqr = board[square_to_index(sqr)]

        if piece_on_sqr == 0:
            available_squares.append(sqr)
           
        elif (piece_on_sqr < 0 and color == 'w') or (piece_on_sqr > 0 and color == 'b'):
            available_squares.append(sqr)
            break

        else:
            break
        
        
    # down-left
    x, y = 0, 0
    while c + x > 97 and rank + y > 1:
        x -= 1
        y -= 1
    
        sqr = f"{chr(c + x)}{rank + y}"
        piece_on_sqr = board[square_to_index(sqr)]

        if piece_on_sqr == 0:
            available_squares.append(sqr)
           
        elif (piece_on_sqr < 0 and color == 'w') or (piece_on_sqr > 0 and color == 'b'):
            available_squares.append(sqr)
            break

        else:
            break
    
    # down-right
    x, y = 0, 0
    while c + x < 104 and rank + y > 1:
        x += 1
        y -= 1
    
        sqr = f"{chr(c + x)}{rank + y}"
        piece_on_sqr = board[square_to_index(sqr)]

        if piece_on_sqr == 0:
            available_squares.append(sqr)
           
        elif (piece_on_sqr < 0 and color == 'w') or (piece_on_sqr > 0 and color == 'b'):
            available_squares.append(sqr)
            break

        else:
            break

    return [(square, to_sqr) for to_sqr in available_squares]
    

if __name__ == "__main__":
    #board = create_starting_position()

    board = create_empty_board()
    
    piece = 5
    board[square_to_index('e4')] = piece
    board[square_to_index('f5')] = -piece
    
    B_moves_a1 = generate_queen_move(board, 'e4')

    print(f"'a1' -> {B_moves_a1}")

    '''
    board[square_to_index('h4')] = -piece
    board[square_to_index('a4')] = -piece
    board[square_to_index('e1')] = -piece
    board[square_to_index('e8')] = -piece

    R_moves_e4 = generate_rook_move(board, 'e4')
    
    print(f"'e4' -> {R_moves_e4}")

    board[square_to_index('e4')] = 2
    N_moves_e4 = generate_knight_move(board, 'e4')
    N_moves_b1 = generate_knight_move(board, 'b1')
    N_moves_g1 = generate_knight_move(board, 'g1')
    N_moves_g8 = generate_knight_move(board, 'g8')
    
    print(f"'b1' -> {N_moves_b1}")
    print(f"'g1' -> {N_moves_g1}")
    print(f"'g8' -> {N_moves_g8}")
    print(f"'e4' -> {N_moves_e4}")

    board[square_to_index('g6')] = 1
    board[square_to_index('f3')] = -1
    
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
       ''' 
        