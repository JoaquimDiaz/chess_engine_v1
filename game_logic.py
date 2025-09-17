import chess_board as cb
import move_generation as mv
import config
import logging

logger = logging.getLogger(__name__)


def generate_pseudo_legal_moves(
    board: list[int], color: int, board_state: config.BoardState
) -> tuple[list[tuple[int, int]], list[list[int]]]:
    """ """
    ...


def generate_legal_moves(
    board: list[int],
    color: int,
    board_state: config.BoardState,
    checking_pieces: list[tuple[int, int]] | None,
    pinned_pieces: list[tuple[int, int]] | None,
    castle_king_side_right: bool,
    castle_queen_side_right: bool,
) -> tuple[list[tuple[int, int]], list[list[int]]]:
    """ """
    # pseudo_legal_move_list = generate_pseudo_legal_moves(board, color, board_state)
    MOVE_GENERATOR = {
        config.PAWN: mv.generate_pawn_moves,
        config.KNIGHT: mv.generate_knight_moves,
        config.BISHOP: mv.generate_bishop_moves,
        config.ROOK: mv.generate_rook_moves,
        config.QUEEN: mv.generate_queen_moves,
        config.KING: mv.generate_king_moves,
    }

    # At least 2 checking pieces ? The king as to move
    # -> return (king, king_legal_moves) immediately
    if checking_pieces is not None and len(checking_pieces) > 1:
        king = (
            (config.WHITE_KING, board_state[4])
            if color == config.WHITE
            else (config.BLACK_KING, board_state[5])
        )
        return (king, mv.generate_king_legal_moves(board, board_state, color))

    # Else we generate `pseudo_legal_moves`
    piece_and_position: list[tuple[int, int]] = []
    list_of_moves: list[list[int]] = []

    pieces_position = board_state[:4]

    piece_list, idx_list = (0, 1) if color == config.WHITE else (2, 3)

    for piece, idx in zip(pieces_position[piece_list], pieces_position[idx_list]):
        list_of_moves = MOVE_GENERATOR[piece](board, idx)

    return (piece_and_position, list_of_moves)


def analyze_castling_rights(): ...


def analyze_king_safety(
    board: list[int], king_square_idx: int, color: int
) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
    """
    Scan for checking pieces and pinned pieces.

    Returns (checking_pieces, pinned_pieces) where each is either a list of tuple or none.
    The tuples inside the list contains (piece, idx).
    """
    if abs(board[king_square_idx]) != config.KING:
        raise ValueError(
            "Can't check for pin/check, piece is not a king: '%i'",
            board[king_square_idx],
        )

    checking_pieces: list[tuple[int, int]] = []
    pinned_pieces: list[tuple[int, int]] = []

    directions = [
        # files
        (0, 1),
        (1, 0),
        (-1, 0),
        (0, -1),
        # diagonals
        (1, 1),
        (-1, 1),
        (1, -1),
        (-1, -1),
    ]

    # ------ SLIDING PIECES ------ #
    for direction in directions:
        checking_piece, pinned_piece = directional_check(
            board, king_square_idx, color, direction
        )
        if checking_piece is not None:
            checking_pieces.append(checking_piece)
        if pinned_piece is not None:
            pinned_pieces.append(pinned_piece)

    # ------ KNIGHT CHECK ------ #
    knight_threat = knight_check(board, color, king_square_idx)
    if knight_threat is not None:
        checking_pieces.append(knight_threat)

    return (checking_pieces, pinned_pieces)


def directional_check(
    board: list[int], idx: int, color: int, direction: tuple[int, int]
) -> tuple[tuple[int, int] | None, tuple[int, int] | None]:
    """
    Scan from `idx` in `direction` and identify:
    - a checking sliding ennemy piece
    - a pinned friendly piece

    Returns (checking_piece, pinned_piece) where each is either a (piece, idx) tuple or None.
    """
    file, rank = cb.parse_index(idx)

    file_delta = direction[0]
    rank_delta = direction[1]

    friendly_piece_idx: int | None = None

    if rank_delta == 0 or file_delta == 0:
        threatening_pieces = [config.ROOK, config.QUEEN]
    else:
        threatening_pieces = [config.BISHOP, config.QUEEN]

    i: int = 0
    while True:
        i += 1

        next_file: int = file + (i * file_delta)
        next_rank: int = rank + (i * rank_delta)

        if not (1 <= next_file <= 8 and 1 <= next_rank <= 8):
            break

        piece_index = cb.parse_coordinates_to_idx(next_file, next_rank)
        piece_on_board = board[piece_index]

        # ------ EMPTY SQUARE ------ #
        ## If square is empty, move to next square
        if piece_on_board == config.EMPTY_SQUARE:
            continue

        # ------ FRIENDLY PIECE ------- #
        ## If a friendly piece is encountered, check if a friendly piece as already been encountered.
        elif (piece_on_board > 0 and color == config.WHITE) or (
            piece_on_board < 0 and color == config.BLACK
        ):
            ## If this is the case, break the loop because there will not be a pin.
            if friendly_piece_idx is not None:
                break
            ## Else add the square index to the varriable friendly_piece.
            if friendly_piece_idx is None:
                friendly_piece_idx = piece_index
                continue

        # ------ ENNEMY PIECE ------ #
        ## If a "threatening piece" is encountered, check:
        elif abs(piece_on_board) in threatening_pieces:
            ## - If there is no friendly_piece then checking_piece
            if friendly_piece_idx is None:
                checking_piece = piece_on_board
                return (checking_piece, piece_index), None
            ## - If there is a friendly_piece then pinned_piece
            else:
                pinned_piece = board[friendly_piece_idx]
                return None, (pinned_piece, friendly_piece_idx)

        ## ------ NON-THREATENING ENNEMY PIECE ------ #
        break

    return None, None


def knight_check(board: list[int], color: int, king_idx: int) -> tuple[int, int] | None:
    """
    Scan possible square for knight checks. If the file or rank is out of bound,
    skip and go to the next coordinates.

    Returns:
        - tuple[int, int] if a knight is found (piece, piece_idx) eg. (2, 8)
        - None if no Knight is found at those coordinates
    """
    file, rank = cb.parse_index(king_idx)

    threatening_piece: int = (
        config.WHITE_KNIGHT if color == config.BLACK else config.BLACK_KNIGHT
    )

    coordinate_list: list[tuple[int, int]] = [
        (1, 2),
        (-1, 2),
        (1, -2),
        (-1, -2),
        (2, 1),
        (-2, 1),
        (2, -1),
        (-2, -1),
    ]

    for file_delta, rank_delta in coordinate_list:
        file_to_scan = file + file_delta
        rank_to_scan = rank + rank_delta

        if not (1 <= file_to_scan <= 8 and 1 <= rank_to_scan <= 8):
            continue

        else:
            piece_idx = cb.parse_coordinates_to_idx(file_to_scan, rank_to_scan)
            piece = board[piece_idx]
            if piece == threatening_piece:
                return (piece, piece_idx)

    return None


if __name__ == "__main__":
    # board = cb.create_empty_board()
    board = cb.create_starting_position()

    board = make_move(board, ("e2", "e4"))
    board = make_move(board, ("e7", "e5"))
    board = make_move(board, ("b1", "c3"))
    board = make_move(board, ("f2", "f4"))
    board = make_move(board, ("d8", "h4"))
    board = make_move(board, ("g2", "g3"))
    board = make_move(board, ("h4", "g3"))

    cb.pretty_display_board(board)

    moves = generate_legal_moves(board, config.WHITE)

    print(moves)

    quit()
    piece_list = mv.find_pieces(board, config.WHITE)
    print(piece_list)

    board[cb.square_to_index("e4")] = 6

    board[cb.square_to_index("e5")] = 4

    board[cb.square_to_index("h7")] = -3

    board[cb.square_to_index("f5")] = 3

    board[cb.square_to_index("e8")] = -4

    board[cb.square_to_index("f6")] = -2

    checking_pieces, pinned_pieces = analyze_king_safety(board, "e4")

    print(f"Checks: {checking_pieces}")
    print(f"Pins: {pinned_pieces}")
