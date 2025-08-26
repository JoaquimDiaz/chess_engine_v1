EMPTY_SQUARE = 0
WHITE_PAWN, BLACK_PAWN = 1, -1
WHITE_KNIGHT, BLACK_KNIGHT = 2, -2
WHITE_BISHOP, BLACK_BISHOP = 3, -3
WHITE_ROOK, BLACK_ROOK = 4, -4
WHITE_KING, BLACK_KING = 5, -5
WHITE_QUEEN, BLACK_QUEEN = 6, -6

EMPTY_CHESS_BOARD = [0] * 64

def main():
    create_chess_board()

def create_chess_board():
    board = EMPTY_CHESS_BOARD
    
    board[0,7] = WHITE_ROOK, WHITE_KNIGHT, WHITE_BISHOP,
    
    board[8,9] = WHITE_PAWN
    

if __name__ == "__main__":
    main()