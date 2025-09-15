import chess_board as cb
import config

board = cb.create_empty_board()

board[cb.square_to_index("a2")] = config.BLACK_BISHOP
board[cb.square_to_index("d5")] = config.WHITE_KING

cb.display_board(board)
