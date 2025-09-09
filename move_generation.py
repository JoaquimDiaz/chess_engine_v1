from chess_board import square_to_index, create_empty_board
import chess_board as cb

import logging

logger = logging.getLogger(__name__)

def generate_pawn_move(board, square, skip_validation=False):
    file = square[0]
    rank = int(square[1])
    piece = board[square_to_index(square)]
    
    if abs(piece) != 1 and not skip_validation:
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

def generate_knight_move(board, square, skip_validation=False):
    file = square[0] 
    rank = int(square[1])
    c = ord(file)
    piece = board[square_to_index(square)]
    color = 'w' if piece > 0 else 'b'

    potential_squares = []
    available_squares = []

    if abs(piece) != 2 and not skip_validation:
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

def generate_rook_move(board, square, skip_validation=False):
    file = square[0]
    rank = int(square[1])
    c = ord(file)
    piece = board[square_to_index(square)]

    if abs(piece) != 4 and not skip_validation:
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

def generate_bishop_move(board, square, skip_validation=False):
    file = square[0]
    rank = int(square[1])
    c = ord(file)
    piece = board[square_to_index(square)]

    available_squares = []
    
    if abs(piece) != 3 and not skip_validation:
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

def generate_queen_move(board, square, skip_validation=False):
    piece = board[square_to_index(square)]

    if abs(piece) != 5 and not skip_validation:
        return []

    move_list = []

    move_list.extend(generate_bishop_move(board, square, skip_validation=True))
    move_list.extend(generate_rook_move(board, square, skip_validation=True))

    return move_list

def generate_king_move(board, square, skip_validation=False):
    file = square[0]
    rank = int(square[1])
    c = ord(file)
    piece = board[square_to_index(square)]
    potential_squares = []
    available_squares = []
    safe_squares = []

    if abs(piece) != 6 and not skip_validation:
        return []
    
    color = 'w' if piece > 0 else 'b'

    potential_squares.append(f"{chr(c - 1)}{rank}")
    potential_squares.append(f"{chr(c + 1)}{rank}")
    potential_squares.append(f"{chr(c - 1)}{rank + 1}")
    potential_squares.append(f"{chr(c - 1)}{rank - 1}")
    potential_squares.append(f"{chr(c + 1)}{rank + 1}")
    potential_squares.append(f"{chr(c + 1)}{rank - 1}")
    potential_squares.append(f"{file}{rank + 1}")
    potential_squares.append(f"{file}{rank - 1}")
    
    for s in potential_squares:
        try:
            piece_on_board = board[square_to_index(s)]
            if piece_on_board == 0:
                available_squares.append(s)
            elif (piece_on_board < 0 and color == 'w') or (piece_on_board > 0 and color == 'b'):
                available_squares.append(s)
            else:
                pass
        except (ValueError, IndexError):
            pass
    
    for s in available_squares:
        if is_safe_square(board, s):
            safe_squares.append(s)

    return [(square, to_sqr) for to_sqr in safe_squares]

def is_safe_square(board: list, square) -> bool:
    """
    Validate the safety of a square for king movement.
    A square is safe is the king can move to this square without being captured.

    Returns:
        bool: True if square is safe else False
    """
    ...

def find_pieces(board: list, color: str) -> list[tuple[int, str]]:
    piece_list = []
    for i in range(64):
        piece = board[i]
        if (piece > 0 and color == 'w') or (piece < 0 and color == 'b'):
            square = cb.index_to_square(i)
            piece_list.append((board[i], square))
    
    return piece_list

def find_king(board: list, color: str) -> str:
    for i in range(64):
        if (board[i] == cb.WHITE_KING and color == 'w') or (board[i] == cb.BLACK_KING and color == 'b'):
            square = cb.index_to_square(i)
            return square
    
    raise ValueError(f"No king found for {color}")
        
def generate_all_moves(board: list, color: str) -> list[tuple[str, str]]:
    """
    Generate all possible moves in a given position for the given piece color.
    
    Returns:
        list of tuple with str
    """
    color_pieces: list = find_pieces(board, color)
    available_moves: list = []

    for piece, square in color_pieces:
        if abs(piece) == cb.WHITE_PAWN:
            available_moves.extend(generate_pawn_move(board, square))
        elif abs(piece) == cb.WHITE_ROOK:
            available_moves.extend(generate_rook_move(board, square))
        elif abs(piece) == cb.WHITE_BISHOP:
            available_moves.extend(generate_bishop_move(board, square))
        elif abs(piece) == cb.WHITE_KNIGHT:
            available_moves.extend(generate_knight_move(board, square))
        elif abs(piece) == cb.WHITE_QUEEN:
            available_moves.extend(generate_queen_move(board, square))
        elif abs(piece) == cb.WHITE_KING:
            available_moves.extend(generate_king_move(board, square))

    return available_moves

if __name__ == "__main__":
    #board = create_starting_position()

    board = create_empty_board()
    
    piece = 6
    board[square_to_index('a1')] = piece
    board[square_to_index('f5')] = piece
    
    B_moves_a1 = generate_king_move(board, 'a1')

    print(f"'a1' -> {B_moves_a1}")
    board = cb.create_starting_position()

    a = find_pieces(board, 'w')
    print(a)
    a = generate_all_moves(board, 'w')
    print(a)
