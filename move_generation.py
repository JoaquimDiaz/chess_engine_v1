import chess_board as cb
import logging

logger = logging.getLogger(__name__)

PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING = (
    cb.WHITE_PAWN,
    cb.WHITE_KNIGHT,
    cb.WHITE_BISHOP,
    cb.WHITE_ROOK,
    cb.WHITE_QUEEN,
    cb.WHITE_KING,
)


def generate_pawn_move(
    board: list[int],
    square: str,
    skip_validation: bool = False,
    return_origin: bool = True,
) -> list[str]:
    """
    Generating a list of valid moves for a pawn.

    Arguments:
        - board: 64 integer list representing the board
        - square: eg. 'a2' where the pawn is
        - skip_validation: wheter to validate if the piece on the square is effectively a pawn
        - return_origin: return a the origin square with the destination square in a tuple

    Returns:
        - list[tuple[str, str]] if `return_origin` is True (from_square, to_square)
        - list[str] if `return_origin` is False list[squares]
    """
    file = square[0]
    rank = int(square[1])
    piece = board[cb.square_to_index(square)]

    if abs(piece) != 1 and not skip_validation:
        return []

    color = "w" if piece > 0 else "b"

    if (color == "w" and rank == 8) or (color == "b" and rank == 1):
        return []

    available_squares: list[str] = []

    # ------ PAWN MOVES ------ #
    sqr1 = f"{file}{rank + 1}" if color == "w" else f"{file}{rank - 1}"
    idx1 = cb.square_to_index(sqr1)
    if board[idx1] == 0:
        available_squares.append(sqr1)

        # If pawns are on their initial square allow to move two squares
        if (color == "w" and rank == 2) or (color == "b" and rank == 7):
            sqr2 = f"{file}{rank + 2}" if color == "w" else f"{file}{rank - 2}"
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
    rank_capture: int = rank + 1 if color == "w" else rank - 1

    capturable_squares = [f"{f}{rank_capture}" for f in files]

    # adding squares to availables squares if there is an ennemy piece
    for s in capturable_squares:
        board_square = board[cb.square_to_index(s)]
        if (board_square < 0 and color == "w") or (board_square > 0 and color == "b"):
            available_squares.append(s)

    if return_origin:
        return [(square, to_sqr) for to_sqr in available_squares]
    else:
        return available_squares


def generate_pawn_attacks(
    board: list[int], square: str, return_origin: bool = True
) -> list[tuple[str, str]] | list[str]:
    """
    Generate diagonal pawn attacking moves. Used for checking if a square is safe for the king to move.
    """
    f, r = cb.parse_square(square)
    attacked_squares: list[str] = []
    color: str = "b" if board[cb.square_to_index(square)] < 0 else "w"

    new_rank = r - 1 if color == "b" else r + 1
    for file_delta in (1, -1):
        new_file = f + file_delta
        if 1 <= new_file <= 8 and 1 <= new_rank <= 8:
            attacked_squares.append(cb.parse_coordinates(new_file, new_rank))
        else:
            continue

    if return_origin:
        return [(square, to_sqr) for to_sqr in attacked_squares]
    else:
        return attacked_squares


def generate_knight_move(
    board: list[int],
    square: str,
    skip_validation: bool = False,
    return_origin: bool = True,
) -> list[tuple[str, str]] | list[str]:
    """ """
    file = square[0]
    rank = int(square[1])
    c = ord(file)
    piece = board[cb.square_to_index(square)]
    color = "w" if piece > 0 else "b"

    potential_squares: list[str] = []
    available_squares: list[str] = []

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
            idx = cb.square_to_index(s)
            if color == "w" and board[idx] <= 0:
                available_squares.append(s)
            if color == "b" and board[idx] >= 0:
                available_squares.append(s)
        except (ValueError, IndexError):
            continue
    if return_origin:
        return [(square, to_sqr) for to_sqr in available_squares]
    else:
        return available_squares


def generate_rook_move(
    board: list[int],
    square: str,
    skip_validation: bool = False,
    return_origin: bool = True,
) -> list[tuple[str, str]] | list[str]:
    """ """
    file = square[0]
    rank = int(square[1])
    c = ord(file)
    piece = board[cb.square_to_index(square)]

    if abs(piece) != 4 and not skip_validation:
        return []

    color = "w" if piece > 0 else "b"

    available_squares: list[str] = []

    ## left
    i = 0
    while c + i > 97:
        i -= 1
        sqr = f"{chr(c + i)}{rank}"
        piece_on_sqr = board[cb.square_to_index(sqr)]
        if piece_on_sqr == 0:
            available_squares.append(sqr)
        elif (piece_on_sqr < 0 and color == "w") or (piece_on_sqr > 0 and color == "b"):
            available_squares.append(sqr)
            break
        else:
            break
    ## right
    i = 0
    while c + i < 104:
        i += 1
        sqr = f"{chr(c + i)}{rank}"
        piece_on_sqr = board[cb.square_to_index(sqr)]
        if piece_on_sqr == 0:
            available_squares.append(sqr)
        elif (piece_on_sqr < 0 and color == "w") or (piece_on_sqr > 0 and color == "b"):
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
        elif (piece_on_sqr < 0 and color == "w") or (piece_on_sqr > 0 and color == "b"):
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
        elif (piece_on_sqr < 0 and color == "w") or (piece_on_sqr > 0 and color == "b"):
            available_squares.append(sqr)
            break
        else:
            break

    if return_origin:
        return [(square, to_sqr) for to_sqr in available_squares]
    else:
        return available_squares


def generate_bishop_move(
    board: list[int],
    square: str,
    skip_validation: bool = False,
    return_origin: bool = True,
) -> list[tuple[str, str]] | list[str]:
    """ """
    file = square[0]
    rank = int(square[1])
    c = ord(file)
    piece = board[cb.square_to_index(square)]

    available_squares: list[str] = []

    if abs(piece) != 3 and not skip_validation:
        return []

    color = "w" if piece > 0 else "b"

    # up-right
    x, y = 0, 0
    while c + x < 104 and rank + y < 8:
        x += 1
        y += 1

        sqr = f"{chr(c + x)}{rank + y}"
        piece_on_sqr = board[cb.square_to_index(sqr)]

        if piece_on_sqr == 0:
            available_squares.append(sqr)

        elif (piece_on_sqr < 0 and color == "w") or (piece_on_sqr > 0 and color == "b"):
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

        elif (piece_on_sqr < 0 and color == "w") or (piece_on_sqr > 0 and color == "b"):
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

        elif (piece_on_sqr < 0 and color == "w") or (piece_on_sqr > 0 and color == "b"):
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

        elif (piece_on_sqr < 0 and color == "w") or (piece_on_sqr > 0 and color == "b"):
            available_squares.append(sqr)
            break

        else:
            break

    if return_origin:
        return [(square, to_sqr) for to_sqr in available_squares]
    else:
        return available_squares


def generate_queen_move(
    board: list[int],
    square: str,
    skip_validation: bool = False,
    return_origin: bool = True,
) -> list[str]:
    """ """
    piece = board[cb.square_to_index(square)]

    if abs(piece) != 5 and not skip_validation:
        return []

    move_list: list[str] = []

    if return_origin:
        move_list.extend(generate_bishop_move(board, square, skip_validation=True))
        move_list.extend(generate_rook_move(board, square, skip_validation=True))

        return move_list
    else:
        move_list.extend(
            generate_bishop_move(
                board, square, skip_validation=True, return_origin=False
            )
        )
        move_list.extend(
            generate_rook_move(board, square, skip_validation=True, return_origin=False)
        )

        return move_list


def generate_king_move(
    board, square, skip_validation=False, return_origin=True
) -> list[tuple[str, str]] | list[str]:
    file = square[0]
    rank = int(square[1])
    c = ord(file)
    piece = board[square_to_index(square)]
    potential_squares = []
    available_squares = []
    safe_squares = []

    if abs(piece) != 6 and not skip_validation:
        return []

    color = "w" if piece > 0 else "b"

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
            elif (piece_on_board < 0 and color == "w") or (
                piece_on_board > 0 and color == "b"
            ):
                available_squares.append(s)
            else:
                pass
        except (ValueError, IndexError):
            pass

    if return_origin:
        return [(square, to_sqr) for to_sqr in available_squares]
    else:
        return available_squares


#    for s in available_squares:
#        if is_safe_square(board, s):
#            safe_squares.append(s)


#    return [(square, to_sqr) for to_sqr in safe_squares]


def is_safe_square(board: list, square) -> bool:
    """
    Validate the safety of a square for king movement.
    A square is safe is the king can move to this square without being captured.

    Returns:
        bool: True if square is safe else False
    """
    ...


def find_pieces(board: list, color: str) -> list[tuple[int, str]]:
    """
    Return a list of tuple with the piece number and associated square.

    Returns:
        list[(piece, square)]
    """
    piece_list = []
    for i in range(64):
        piece = board[i]
        if (piece > 0 and color == "w") or (piece < 0 and color == "b"):
            square = cb.index_to_square(i)
            piece_list.append((board[i], square))

    return piece_list


def find_king(board: list, color: str) -> str:
    """
    Find the king's on the board and returns the associated square.

    Raises:
        ValueError if the king for the given color is not found.
    """
    for i in range(64):
        if (board[i] == cb.WHITE_KING and color == "w") or (
            board[i] == cb.BLACK_KING and color == "b"
        ):
            square = cb.index_to_square(i)
            return square

    raise ValueError(f"No king found for {color}")


def generate_attacked_squares(
    board: list, color: str, return_origin=True
) -> list[tuple[str, str]]:
    """
    Generate all possible moves in a position for the given piece color.

    Returns:
        list of tuple with str
    """
    MOVE_GENERATOR = {
        PAWN: generate_pawn_attacks,
        KNIGHT: generate_knight_move,
        BISHOP: generate_bishop_move,
        ROOK: generate_rook_move,
        QUEEN: generate_queen_move,
        KING: generate_king_move,
    }

    color_pieces: list = find_pieces(board, color)
    attacked_squares: list = []

    for piece, square in color_pieces:
        generator = MOVE_GENERATOR[abs(piece)]
        attacked_squares.extend(generator(board, square, return_origin=return_origin))

    return attacked_squares


def generate_king_legal_move(
    board: list, color: str, return_origin=True
) -> list[tuple[str, str] | list[str]]:
    """
    Generate legal moves for the king by filtering with the list of square controlled by the opponent pieces.

    Returns:
        - list of tuple if returns_origin is True: (king_square, to_square)
        - list of the squares if returns_origin is False
    """
    legal_moves: list = []
    king_square: str = find_king(board, color)
    available_moves: list = generate_king_move(board, king_square, return_origin=False)

    opponent_color: str = "b" if color == "w" else "w"
    attacked_squares = set(
        generate_attacked_squares(board, opponent_color, return_origin=False)
    )

    for s in available_moves:
        if s not in attacked_squares:
            legal_moves.append(s)

    if return_origin:
        return [(king_square, to_sqr) for to_sqr in legal_moves]
    else:
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

    a = generate_attacked_squares(board, "w", False)
    print(a)

    a = generate_pawn_attacks(board, "g2", return_origin=False)
    print(a)

    a = generate_king_legal_move(board, "b", return_origin=False)
    print(a)
