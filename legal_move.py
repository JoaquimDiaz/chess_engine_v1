import chess_board
import move_generation

def analyze_king_safety(board, king_square):
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
    
    return checking_pieces, pinned_pieces
     
                
def directional_check(board: list, file: str, rank: int, color: str, file_delta: int, rank_delta: int): #-> tuple[str | None, str | None]:
    c: int = ord(file)
    checking_piece: str = None
    friendly_piece: str = None

    if rank_delta == 0 or file_delta == 0:
        threatning_pieces = [chess_board.WHITE_ROOK, chess_board.WHITE_QUEEN]
    else:
        threatning_pieces = [chess_board.WHITE_BISHOP, chess_board.WHITE_QUEEN]
    
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
        ## threatning piece
        elif abs(piece_on_board) in threatning_pieces:
            if not friendly_piece:
                checking_piece = sqr
                return checking_piece, friendly_piece
            if friendly_piece:
                return checking_piece, friendly_piece
        ## non-threatning piece
        else:
            break
        
    return None, None
            
if __name__ == "__main__":
    board = chess_board.create_empty_board()
    
    board[chess_board.square_to_index('e4')] = 6

    board[chess_board.square_to_index('e5')] = 4

    board[chess_board.square_to_index('h7')] = -3

    board[chess_board.square_to_index('f5')] = 3

    board[chess_board.square_to_index('e8')] = -4

    checking_pieces, pinned_pieces = analyze_king_safety(board, 'e4')

    print(f"Checks: {checking_pieces}")
    print(f"Pins: {pinned_pieces}")
    
    