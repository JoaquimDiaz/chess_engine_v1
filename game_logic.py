import chess_board as cb
import move_generation as mv
import logging

from config import (
    Piece,
    PieceMoves,
    CastlingState,
    WHITE,
    BLACK,
    EMPTY_SQUARE,
    PAWN,
    KNIGHT,
    BISHOP,
    ROOK,
    QUEEN,
    KING,
    WHITE_PAWN,
    WHITE_KNIGHT,
    WHITE_BISHOP,
    WHITE_ROOK,
    WHITE_QUEEN,
    WHITE_KING,
    BLACK_PAWN,
    BLACK_KNIGHT,
    BLACK_BISHOP,
    BLACK_ROOK,
    BLACK_QUEEN,
    BLACK_KING,
    PinnedPiece,
)

logger = logging.getLogger(__name__)


def analyze_king_safety(
    board: list[int], king_square_idx: int, color: int
) -> tuple[list[Piece], list[PinnedPiece]]:
    """
    Scan for checking pieces and pinned pieces.

    If multiple checking pieces are found at some point,
    terminate and return only the checking pieces.
    -> the king has to move so pinned pieces dont matter
    """
    if abs(board[king_square_idx]) != KING:
        raise ValueError(
            "Can't check for pin/check, piece is not a king",
        )

    file, rank = cb.parse_index(king_square_idx)

    checking_pieces: list[Piece] = []
    pinned_pieces: list[PinnedPiece] = []
    check_count: int = 0

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

    # ------ KNIGHT CHECK ------ #
    knight_threat = knight_check(board, file, rank, color)
    if knight_threat is not None:
        checking_pieces.append(knight_threat)
        check_count += 1

    # ------ PAWN CHECK ------ #
    pawn_delta = [(1, 1), (-1, 1)] if color == WHITE else [(1, -1), (-1, -1)]

    threatening_piece = BLACK_PAWN if color == WHITE else WHITE_PAWN
    for file_delta, rank_delta in pawn_delta:
        new_file = file + file_delta
        new_rank = rank + rank_delta
        if new_file > 8 or new_file < 1 or new_rank > 8 or new_rank < 1:
            continue
        square_idx = cb.parse_coordinates_to_idx(new_file, new_rank)
        piece_on_board = board[square_idx]

        if piece_on_board == threatening_piece:
            checking_pieces.append(Piece(piece_on_board, square_idx))
            check_count += 1

    if check_count > 1:
        return (checking_pieces, pinned_pieces)

    # ------ SLIDING PIECES ------ #

    for direction in directions:
        checking_piece, pinned_piece = directional_check(
            board, color, file, rank, direction
        )
        if checking_piece is not None:
            checking_pieces.append(checking_piece)
            check_count += 1

        if check_count > 1:
            return (checking_pieces, pinned_pieces)

        if pinned_piece is not None:
            pinned_pieces.append(pinned_piece)

    return (checking_pieces, pinned_pieces)


def directional_check(
    board: list[int], file: int, rank: int, color: int, direction: tuple[int, int]
) -> tuple[Piece | None, PinnedPiece | None]:
    """
    Scan from `idx` in `direction` and identify:
    - a checking sliding ennemy piece
    - a pinned friendly piece

    Returns (checking_piece, pinned_piece) where each is either a (piece, idx) tuple or None.
    """

    file_delta = direction[0]
    rank_delta = direction[1]

    friendly_piece_idx: int | None = None

    if rank_delta == 0 or file_delta == 0:
        threatening_pieces = [ROOK, QUEEN]
    else:
        threatening_pieces = [BISHOP, QUEEN]

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
        if piece_on_board == EMPTY_SQUARE:
            continue

        # ------ FRIENDLY PIECE ------- #
        ## If a friendly piece is encountered, check if a friendly piece as already been encountered.
        elif (piece_on_board > 0 and color == WHITE) or (
            piece_on_board < 0 and color == BLACK
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
                return Piece(checking_piece, piece_index), None
            ## - If there is a friendly_piece then pinned_piece
            else:
                friendly_piece = Piece(board[friendly_piece_idx], friendly_piece_idx)
                ennemy_piece_idx = piece_index
                return None, PinnedPiece(friendly_piece, direction, ennemy_piece_idx)

        ## ------ NON-THREATENING ENNEMY PIECE ------ #
        break

    return None, None


def knight_check(board: list[int], file: int, rank: int, color: int) -> Piece | None:
    """
    Scan possible square for knight checks. If the file or rank is out of bound,
    skip and go to the next coordinates.

    Returns:
        - tuple[int, int] if a knight is found (piece, piece_idx) eg. (2, 8)
        - None if no Knight is found at those coordinates
    """
    threatening_piece: int = WHITE_KNIGHT if color == BLACK else BLACK_KNIGHT

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
                return Piece(piece, piece_idx)

    return None


if __name__ == "__main__":
    ...
