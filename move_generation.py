from typing import Literal
import chess_board as cb
import config
import logging

logger = logging.getLogger(__name__)


def generate_pawn_moves(
    board: list[int],
    square: str,
) -> list[str]:
    """
    Generating a list of valid moves for a pawn.

    Arguments:
        - board: 64 integer list representing the board
        - square: eg. 'a2' where the pawn is
    """
    file = square[0]
    rank = int(square[1])
    piece = board[cb.square_to_index(square)]

    color = config.WHITE if piece > 0 else config.BLACK

    # Promotion if pawn is on last rank
    if (color == config.WHITE and rank == 8) or (color == config.BLACK and rank == 1):
        return []

    available_squares: list[str] = []

    # ------ PAWN MOVES ------ #
    sqr1 = f"{file}{rank + 1}" if color == config.WHITE else f"{file}{rank - 1}"
    idx1 = cb.square_to_index(sqr1)
    if board[idx1] == 0:
        available_squares.append(sqr1)

        # If pawns are on their initial square allow to move two squares
        if (color == config.WHITE and rank == 2) or (
            color == config.BLACK and rank == 7
        ):
            sqr2 = f"{file}{rank + 2}" if color == config.WHITE else f"{file}{rank - 2}"
            idx2 = cb.square_to_index(sqr2)
            if board[idx2] == 0:
                available_squares.append(sqr2)

    # ------ PAWN CAPTURES ------ #

    # creating a list of available files
    c: int = ord(file)
    files: list[str] = []

    if c != ord("h"):
        files.append(chr(c + 1))

    if c != ord("a"):
        files.append(chr(c - 1))

    # defining rank up or down from color
    rank_capture: int = rank + 1 if color == config.WHITE else rank - 1

    capturable_squares = [f"{f}{rank_capture}" for f in files]

    # adding squares to availables squares if there is an ennemy piece
    for s in capturable_squares:
        board_square = board[cb.square_to_index(s)]
        if (board_square < 0 and color == config.WHITE) or (
            board_square > 0 and color == config.BLACK
        ):
            available_squares.append(s)

    return available_squares


def generate_knight_moves(
    board: list[int],
    square: str,
) -> list[str]:
    """ """
    file = square[0]
    rank = int(square[1])
    c = ord(file)
    piece = board[cb.square_to_index(square)]
    color = config.WHITE if piece > 0 else config.BLACK

    potential_squares: list[str] = []
    available_squares: list[str] = []

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
            idx = cb.square_to_index(s)
            if color == config.WHITE and board[idx] <= 0:
                available_squares.append(s)
            if color == config.BLACK and board[idx] >= 0:
                available_squares.append(s)
        except (ValueError, IndexError):
            continue
    else:
        return available_squares


def generate_rook_moves(board: list[int], square: str) -> list[str]:
    """ """
    file = square[0]
    rank = int(square[1])
    c = ord(file)
    piece = board[cb.square_to_index(square)]

    color = config.WHITE if piece > 0 else config.BLACK

    available_squares: list[str] = []

    ## Left
    i = 0
    while c + i > 97:
        i -= 1
        sqr = f"{chr(c + i)}{rank}"
        piece_on_sqr = board[cb.square_to_index(sqr)]
        if piece_on_sqr == 0:
            available_squares.append(sqr)
        elif (piece_on_sqr < 0 and color == config.WHITE) or (
            piece_on_sqr > 0 and color == config.BLACK
        ):
            available_squares.append(sqr)
            break
        else:
            break
    ## Right
    i = 0
    while c + i < 104:
        i += 1
        sqr = f"{chr(c + i)}{rank}"
        piece_on_sqr = board[cb.square_to_index(sqr)]
        if piece_on_sqr == 0:
            available_squares.append(sqr)
        elif (piece_on_sqr < 0 and color == config.WHITE) or (
            piece_on_sqr > 0 and color == config.BLACK
        ):
            available_squares.append(sqr)
            break
        else:
            break

    ## up
    i = 0
    while rank + i < 8:
        i += 1
        sqr = f"{file}{rank + i}"
        piece_on_sqr = board[cb.square_to_index(sqr)]
        if piece_on_sqr == 0:
            available_squares.append(sqr)
        elif (piece_on_sqr < 0 and color == config.WHITE) or (
            piece_on_sqr > 0 and color == config.BLACK
        ):
            available_squares.append(sqr)
            break
        else:
            break

    ## down
    i = 0
    while rank + i > 1:
        i -= 1
        sqr = f"{file}{rank + i}"
        piece_on_sqr = board[cb.square_to_index(sqr)]
        if piece_on_sqr == 0:
            available_squares.append(sqr)
        elif (piece_on_sqr < 0 and color == config.WHITE) or (
            piece_on_sqr > 0 and color == config.BLACK
        ):
            available_squares.append(sqr)
            break
        else:
            break

    return available_squares


def generate_bishop_moves(board: list[int], square: str) -> list[str]:
    """ """
    file = square[0]
    rank = int(square[1])
    c = ord(file)
    piece = board[cb.square_to_index(square)]

    available_squares: list[str] = []

    color = config.WHITE if piece > 0 else config.BLACK

    # up-right
    x, y = 0, 0
    while c + x < 104 and rank + y < 8:
        x += 1
        y += 1

        sqr = f"{chr(c + x)}{rank + y}"
        piece_on_sqr = board[cb.square_to_index(sqr)]

        if piece_on_sqr == 0:
            available_squares.append(sqr)

        elif (piece_on_sqr < 0 and color == config.WHITE) or (
            piece_on_sqr > 0 and color == config.BLACK
        ):
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
        piece_on_sqr = board[cb.square_to_index(sqr)]

        if piece_on_sqr == 0:
            available_squares.append(sqr)

        elif (piece_on_sqr < 0 and color == config.WHITE) or (
            piece_on_sqr > 0 and color == config.BLACK
        ):
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
        piece_on_sqr = board[cb.square_to_index(sqr)]

        if piece_on_sqr == 0:
            available_squares.append(sqr)

        elif (piece_on_sqr < 0 and color == config.WHITE) or (
            piece_on_sqr > 0 and color == config.BLACK
        ):
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
        piece_on_sqr = board[cb.square_to_index(sqr)]

        if piece_on_sqr == 0:
            available_squares.append(sqr)

        elif (piece_on_sqr < 0 and color == config.WHITE) or (
            piece_on_sqr > 0 and color == config.BLACK
        ):
            available_squares.append(sqr)
            break

        else:
            break

    return available_squares


def generate_pawn_attacks(board: list[int], square: str) -> list[str]:
    """
    Generate the list of squares attacked by a pawn.
    """
    file, rank = cb.parse_square(square)
    attacked_squares: list[str] = []
    color = config.WHITE if board[cb.square_to_index(square)] > 0 else config.BLACK

    new_rank = rank + 1 if color == config.WHITE else rank - 1

    for file_delta in (1, -1):
        new_file = file + file_delta
        if 1 <= new_file <= 8 and 1 <= new_rank <= 8:
            attacked_squares.append(cb.parse_coordinates(new_file, new_rank))

    return attacked_squares


def generate_queen_moves(
    board: list[int],
    square: str,
) -> list[str]:
    """
    Generate the list of available squares for a queen.
    Using the 2 functions to generate moves for the rook and the bishop.
    """
    move_list: list[str] = []

    move_list.extend(generate_bishop_moves(board, square))
    move_list.extend(generate_rook_moves(board, square))

    return move_list


def generate_king_moves(board: list[int], square_idx: int) -> list[str]:
    square = cb.index_to_square(square_idx)
    file = square[0]
    rank = int(square[1])
    c = ord(file)
    piece = board[cb.square_to_index(square)]
    potential_squares: list[str] = []
    available_squares: list[str] = []

    color = config.WHITE if piece > 0 else config.BLACK

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
            piece_on_board = board[cb.square_to_index(s)]
            if piece_on_board == 0:
                available_squares.append(s)
            elif (piece_on_board < 0 and color == config.WHITE) or (
                piece_on_board > 0 and color == config.BLACK
            ):
                available_squares.append(s)
            else:
                pass
        except (ValueError, IndexError):
            pass

    return available_squares


def generate_attacked_squares(board: list[int], color: Literal[1, 0]) -> list[str]:
    """
    Generate all possible moves in a position for the given piece color.

    Returns:
        list of tuple with str
    """
    MOVE_GENERATOR = {
        config.PAWN: generate_pawn_attacks,
        config.KNIGHT: generate_knight_moves,
        config.BISHOP: generate_bishop_moves,
        config.ROOK: generate_rook_moves,
        config.QUEEN: generate_queen_moves,
        config.KING: generate_king_moves,
    }

    color_pieces: list = find_pieces(board, color)
    attacked_squares: list = []

    for piece, square in color_pieces:
        generator = MOVE_GENERATOR[abs(piece)]
        attacked_squares.extend(generator(board, square))

    return attacked_squares


def generate_king_legal_moves(
    board: list[int],
    board_state: config.BoardState,
    color: Literal[1, 0],
) -> list[str]:
    """
    Generate legal moves for the king by filtering with the list of square controlled by the opponent pieces.
    """
    legal_moves: list[str] = []
    king_idx = board_state[4] if color == config.WHITE else board_state[5]
    available_moves: list[str] = generate_king_moves(board, king_idx)

    opponent_color: int = config.BLACK if color == config.WHITE else config.WHITE
    attacked_squares = set(generate_attacked_squares(board, opponent_color))

    for s in available_moves:
        if s not in attacked_squares:
            legal_moves.append(s)

    return legal_moves


def generate_all_moves(board: list, color: str, return_origin: bool = True) -> list:
    MOVE_GENERATOR = {
        PAWN: generate_pawn_move,
        KNIGHT: generate_knight_move,
        BISHOP: generate_bishop_move,
        ROOK: generate_rook_move,
        QUEEN: generate_queen_move,
        KING: generate_king_move,
    }

    available_moves: list = []
    player_pieces: list = find_pieces()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    board = cb.create_starting_position()
    board = cb.create_empty_board()

    board[square_to_index("g4")] = -6
    board[square_to_index("g2")] = 1

    cb.display_board(board)

    a = generate_attacked_squares(board, config.WHITE, False)
    print(a)

    a = generate_pawn_attacks(board, "g2", return_origin=False)
    print(a)

    a = generate_king_legal_move(board, config.BLACK, return_origin=False)
    print(a)
