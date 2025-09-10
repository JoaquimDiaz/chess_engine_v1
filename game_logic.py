import chess_board
import move_generation
from move_generation import find_king, find_pieces, generate_all_moves
import logging

logger = logging.getLogger(__name__)

def make_move(board: list, move: tuple[str, str]) -> list:
    new_board = board.copy()
    piece = board[chess_board.square_to_index(move[0])] 

    new_board[chess_board.square_to_index(move[0])] = chess_board.EMPTY_SQUARE
    new_board[chess_board.square_to_index(move[1])] = piece

    return new_board

def generate_legal_moves(board: list, color: str):
    """
    ?? Generating all possible moves and then filtering with king safety considerations ?
    """
    king_square: str = find_king(board, color)
    checking_pieces, pinned_pieces = analyze_king_safety(board, king_square)
    
    if checking_pieces:
        handle_checks(board, color, king_square, checking_pieces)

    all_moves = generate_all_moves(board, color)    

    print(checking_pieces)
    print(pinned_pieces)

def handle_checks(board:list, colors: str, king_square: str, checking_pieces: set):
    nb_check = len(checking_pieces)
    # Raise error if no checking pieces in set
    if nb_check == 0:
        raise ValueError("No checking pieces in set")
        
    # Handle case where 1 piece is checking the king
    # - You can move the king, take the checking piece or block the check
    elif nb_check == 1:
        king_file = king_square[0]
        king_rank = int(king_square[1])
        
        if checking_pieces:
            ...

    # Handle case where more than 1 piece is checking the king.
    # - The king has to move
    elif nb_check > 1:
        # generate_king_moves()
        ...
    
def analyze_king_safety(board: list, king_square: str) -> tuple[set, set]:
    file = king_square[0]
    rank = int(king_square[1])
    piece = board[chess_board.square_to_index(king_square)]
    
    if abs(piece) != chess_board.WHITE_KING:
        raise ValueError(f"Can't check for pin/check, piece is not a king: '{piece}'")

    color = 'w' if piece > 0 else 'b'
    
    checking_pieces: set = set()
    pinned_pieces: set = set()

    directions = [
        (0, 1), (1, 0), (-1, 0), (0, -1), # files
        (1, 1), (-1, 1), (1, -1), (-1, -1) # diagonals
    ]
    
    for file_delta, rank_delta in directions:
        checking_piece, pinned_piece = directional_check(board, file, rank, color, file_delta, rank_delta)
        if checking_piece:
            checking_pieces.add(checking_piece)
        if pinned_piece:
            pinned_pieces.add(pinned_piece)
    
    knight_threat = knight_check(board, color, file, rank)
    if knight_threat:
        checking_pieces.add(knight_threat)
    
    return checking_pieces, pinned_pieces
     
                
def directional_check(board: list, file: str, rank: int, color: str, file_delta: int, rank_delta: int): #-> tuple[str | None, str | None]:
    c: int = ord(file)
    checking_piece: str = None
    friendly_piece: str = None

    if rank_delta == 0 or file_delta == 0:
        threatening_pieces = [chess_board.WHITE_ROOK, chess_board.WHITE_QUEEN]
    else:
        threatening_pieces = [chess_board.WHITE_BISHOP, chess_board.WHITE_QUEEN]
    
    i: int = 0
    while True:
        i += 1
        
        next_file: int = c + (i * file_delta)
        next_rank: int = rank + (i * rank_delta)

        if next_rank > 8 or next_rank < 1 or next_file > 104 or next_file < 97:
            break
        
        sqr: str = f"{chr(next_file)}{next_rank}"
        piece_on_board: int = board[chess_board.square_to_index(sqr)]
        
        # ------ empty square ------ #
        if piece_on_board == chess_board.EMPTY_SQUARE:
            continue

        # ------ friendly piece ------- #
        elif (piece_on_board > 0 and color == 'w') or (piece_on_board < 0 and color == 'b'):
            if friendly_piece:
                break
            if not friendly_piece:
                friendly_piece = sqr
                continue
            
        # ------ ennemy piece ------ #
        ## threatening piece
        elif abs(piece_on_board) in threatening_pieces:
            if not friendly_piece:
                checking_piece = sqr
                return checking_piece, friendly_piece
            if friendly_piece:
                return checking_piece, friendly_piece
        ## non-threatening piece
        else:
            break
        
    return None, None

def knight_check(board: list, color: str, file: str, rank: int):
    c = ord(file)
    threatening_piece: int = chess_board.WHITE_KNIGHT if color == 'b' else chess_board.BLACK_KNIGHT

    squares_to_check: list = [
        f"{chr(c + 1)}{rank + 2}",
        f"{chr(c - 1)}{rank + 2}",
        f"{chr(c + 1)}{rank - 2}",
        f"{chr(c - 1)}{rank - 2}",
        f"{chr(c + 2)}{rank + 1}",
        f"{chr(c - 2)}{rank + 1}",
        f"{chr(c + 2)}{rank - 1}",
        f"{chr(c - 2)}{rank - 1}",
    ]

    for sqr in squares_to_check:
        try:
            piece_on_board = board[chess_board.square_to_index(sqr)]
            if piece_on_board == threatening_piece:
                return sqr
        except (ValueError, IndexError):
            pass 
    
    return None        

if __name__ == "__main__":
    #board = chess_board.create_empty_board()
    board = chess_board.create_starting_position()
    
    board = make_move(board, ('e2', 'e4'))
    board = make_move(board, ('e7', 'e5'))
    board = make_move(board, ('b1', 'c3'))
    board = make_move(board, ('f2', 'f4'))
    board = make_move(board, ('d8', 'h4'))
    board = make_move(board, ('g2', 'g3'))
    board = make_move(board, ('h4', 'g3'))
    
    chess_board.pretty_display_board(board)
    
    moves = generate_legal_moves(board, 'w')

    print(moves)
    
    quit()
    piece_list = find_pieces(board, 'w')
    print(piece_list)
    
    board[chess_board.square_to_index('e4')] = 6

    board[chess_board.square_to_index('e5')] = 4

    board[chess_board.square_to_index('h7')] = -3

    board[chess_board.square_to_index('f5')] = 3

    board[chess_board.square_to_index('e8')] = -4

    board[chess_board.square_to_index('f6')] = -2

    checking_pieces, pinned_pieces = analyze_king_safety(board, 'e4')

    print(f"Checks: {checking_pieces}")
    print(f"Pins: {pinned_pieces}")
    
    