EMPTY_SQUARE = 0
WHITE_PAWN, BLACK_PAWN = 1, -1
WHITE_KNIGHT, BLACK_KNIGHT = 2, -2
WHITE_BISHOP, BLACK_BISHOP = 3, -3
WHITE_ROOK, BLACK_ROOK = 4, -4
WHITE_QUEEN, BLACK_QUEEN = 5, -5
WHITE_KING, BLACK_KING = 6, -6

PIECE_SYMBOLS = {
    EMPTY_SQUARE: "·",  
    WHITE_PAWN:   "♙", BLACK_PAWN:   "♟",
    WHITE_KNIGHT: "♘", BLACK_KNIGHT: "♞",
    WHITE_BISHOP: "♗", BLACK_BISHOP: "♝",
    WHITE_ROOK:   "♖", BLACK_ROOK:   "♜",
    WHITE_QUEEN:  "♕", BLACK_QUEEN:  "♛",
    WHITE_KING:   "♔", BLACK_KING:   "♚",
}

PIECE_NAMES = {
    0: '.', 1: 'P', -1: 'p', 2: 'N', -2: 'n', 
    3: 'B', -3: 'b', 4: 'R', -4: 'r',
    5: 'Q', -5: 'q', 6: 'K', -6: 'k'
}

def create_chess_board():
    board = [0] * 64
    
    board[0:8] = [WHITE_ROOK, WHITE_KNIGHT, WHITE_BISHOP, WHITE_QUEEN, WHITE_KING, WHITE_BISHOP, WHITE_KNIGHT, WHITE_ROOK]
    
    board[8:16] = [WHITE_PAWN] * 8

    board[48:56] = [BLACK_PAWN] * 8
    
    board[56:64] = [BLACK_ROOK, BLACK_KNIGHT, BLACK_BISHOP, BLACK_QUEEN, BLACK_KING, BLACK_BISHOP, BLACK_KNIGHT, BLACK_ROOK]

    return board

def display_board(board):
    print("    a b c d e f g h")
    print("    ---------------")
    for rank in range(7, -1, -1):  
        print(f"{rank + 1} | ", end="")
        for file in range(8):
            square = rank * 8 + file
            print(f"{PIECE_NAMES[board[square]]} ", end="")
        print(f"| {rank + 1}")
    print("    ---------------")
    print("    a b c d e f g h")
   
def pretty_display_board(board):
    print("   a b c d e f g h")
    print("   ----------------")
    for rank in range(8, 0, -1):
            row = board[(rank-1)*8 : rank*8]
            symbols = [PIECE_SYMBOLS[p] for p in row]
            print(f"{rank} |{' '.join(symbols)} | {rank}")

    print("   ----------------")
    print("   a b c d e f g h")

if __name__ == "__main__":
    board = create_chess_board()

    print("Chess board: ")
    display_board(board)
    
    print("____________")
    print(" ")
    
    print("Pretty chess board: ")
    pretty_display_board(board)
    