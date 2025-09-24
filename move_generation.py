import chess_board as cb
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
    WHITE_KING,
    BLACK_KING,
    PinnedPiece,
)

logger = logging.getLogger(__name__)


def generate_pawn_moves(
    board: list[int], square_idx: int, color: int, en_passant_target: int | None = None
) -> list[int]:
    """
    Generating a list of valid moves for a pawn.

    - If pawns are on their initial square, check for 2 moves.
    - Check diagonal squares for captures
    - en_passant_target if there is an opportunity for en passant capture

    Returns:
    - list[int] corresponding to board idx.
    """
    file, rank = cb.parse_index(square_idx)
    available_squares: list[int] = []
    rank_delta: int = 1 if color == WHITE else -1

    # ------ PAWN MOVES ------ #

    idx1 = cb.parse_coordinates_to_idx(file, rank + rank_delta)
    if board[idx1] == EMPTY_SQUARE:
        available_squares.append(idx1)

        # If pawns are on their initial square allow to move two squares
        if (color == WHITE and rank == 2) or (color == BLACK and rank == 7):
            idx2 = cb.parse_coordinates_to_idx(file, rank + rank_delta * 2)
            if board[idx2] == EMPTY_SQUARE:
                available_squares.append(idx2)
    # -> return a flag for `en passant` when pawn moves two squares ?

    # ------ PAWN CAPTURES ------ #

    # creating a list of available files

    new_rank: int = rank + rank_delta
    for file_delta in (1, -1):
        new_file: int = file + file_delta
        if new_file > 8 or new_file < 1:
            continue
        s_idx = cb.parse_coordinates_to_idx(new_file, new_rank)
        piece_on_board = board[s_idx]
        # en_passant_target? -> check if its the same as the pawn capture
        if en_passant_target is not None and en_passant_target == s_idx:
            available_squares.append(s_idx)
        elif (piece_on_board < 0 and color == WHITE) or (
            piece_on_board > 0 and color == BLACK
        ):
            available_squares.append(s_idx)

    return available_squares


def generate_pawn_controlled_squares(
    board: list[int], square_idx: int, color: int
) -> list[int]:
    """
    Generate attacked squares for a pawn, 1 or 2 diagonal squares.
    """
    file, rank = cb.parse_index(square_idx)
    attacked_squares: list[int] = []

    rank_delta = 1 if color == WHITE else -1
    new_rank = rank + rank_delta

    for file_delta in (1, -1):
        new_file = file + file_delta
        if new_file > 8 or new_file < 1:
            continue
        s_idx = cb.parse_coordinates_to_idx(new_file, new_rank)
        attacked_squares.append(s_idx)

    return attacked_squares


def generate_knight_moves(board: list[int], square_idx: int, color: int) -> list[int]:
    """ """
    file, rank = cb.parse_index(square_idx)

    available_squares: list[int] = []

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

    for coordinate in coordinate_list:
        file_delta, rank_delta = coordinate
        new_file = file + file_delta
        new_rank = rank + rank_delta

        if (new_file > 8 or new_file < 1) or (new_rank > 8 or new_rank < 1):
            continue

        idx = cb.parse_coordinates_to_idx(new_file, new_rank)

        target_square = board[idx]

        if (
            target_square == EMPTY_SQUARE
            or (target_square < 0 and color == WHITE)
            or (target_square > 0 and color == BLACK)
        ):
            available_squares.append(idx)

    return available_squares


def generate_knight_controlled_squares(
    board: list[int], square_idx: int, color: int
) -> list[int]:
    """
    Generate a list of controlled squares for a knight.
    - `EMPTY_SQUARE`
    - Same color piece (for generating legal king move)
    - Ennemy pieces are not added to conrolled squares
        -> ennemy king cant capture them
    """
    file, rank = cb.parse_index(square_idx)

    attacked_squares: list[int] = []

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

    for coordinate in coordinate_list:
        file_delta, rank_delta = coordinate
        new_file = file + file_delta
        new_rank = rank + rank_delta

        if (new_file > 8 or new_file < 1) or (new_rank > 8 or new_rank < 1):
            continue

        idx = cb.parse_coordinates_to_idx(new_file, new_rank)
        piece_on_board = board[idx]

        if piece_on_board == EMPTY_SQUARE:
            attacked_squares.append(idx)

        elif (piece_on_board > 0 and color == WHITE) or (
            piece_on_board < 0 and color == BLACK
        ):
            attacked_squares.append(idx)

        else:
            continue

    return attacked_squares


def generate_rook_moves(board: list[int], square_idx: int, color: int) -> list[int]:
    """ """
    file, rank = cb.parse_index(square_idx)
    available_squares: list[int] = []

    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    for file_delta, rank_delta in directions:
        i = 1
        while True:
            new_file = file + (i * file_delta)
            new_rank = rank + (i * rank_delta)

            if new_file > 8 or new_file < 1 or new_rank > 8 or new_rank < 1:
                break

            next_square: int = cb.parse_coordinates_to_idx(new_file, new_rank)
            piece_on_square: int = board[next_square]

            if piece_on_square == EMPTY_SQUARE:
                available_squares.append(next_square)
                i += 1

            elif (color == WHITE and piece_on_square < 0) or (
                color == BLACK and piece_on_square > 0
            ):
                available_squares.append(next_square)
                break

            else:
                break

    return available_squares


def generate_rook_controlled_squares(
    board: list[int], square_idx: int, color: int
) -> list[int]:
    """ """
    file, rank = cb.parse_index(square_idx)
    attacked_squares: list[int] = []

    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    for file_delta, rank_delta in directions:
        i = 1
        while True:
            new_file = file + (i * file_delta)
            new_rank = rank + (i * rank_delta)

            if new_file > 8 or new_file < 1 or new_rank > 8 or new_rank < 1:
                break

            next_square: int = cb.parse_coordinates_to_idx(new_file, new_rank)
            piece_on_square: int = board[next_square]

            if piece_on_square == EMPTY_SQUARE:
                attacked_squares.append(next_square)
                i += 1

            elif (piece_on_square == BLACK_KING and color == WHITE) or (
                piece_on_square == WHITE_KING and color == BLACK
            ):
                attacked_squares.append(next_square)
                i += 1
                continue

            elif (color == WHITE and piece_on_square < 0) or (
                color == BLACK and piece_on_square > 0
            ):
                break

            else:
                attacked_squares.append(next_square)
                break

    return attacked_squares


def generate_bishop_moves(board: list[int], square_idx: int, color: int) -> list[int]:
    """ """
    file, rank = cb.parse_index(square_idx)
    available_squares: list[int] = []

    directions: list[tuple[int, int]] = [(1, 1), (-1, 1), (1, -1), (-1, -1)]

    for file_delta, rank_delta in directions:
        i = 1
        while True:
            next_file = file + (i * file_delta)
            next_rank = rank + (i * rank_delta)

            if next_file < 1 or next_file > 8 or next_rank < 1 or next_rank > 8:
                break

            next_square = cb.parse_coordinates_to_idx(next_file, next_rank)
            piece_on_board: int = board[next_square]

            if piece_on_board == EMPTY_SQUARE:
                available_squares.append(next_square)
                i += 1

            elif (color == WHITE and piece_on_board < 0) or (
                color == BLACK and piece_on_board > 0
            ):
                available_squares.append(next_square)
                break

            else:
                break

    return available_squares


def generate_bishop_controlled_squares(
    board: list[int], square_idx: int, color: int
) -> list[int]:
    """ """
    file, rank = cb.parse_index(square_idx)
    attacked_squares: list[int] = []

    directions: list[tuple[int, int]] = [(1, 1), (-1, 1), (1, -1), (-1, -1)]

    for file_delta, rank_delta in directions:
        i = 1
        while True:
            next_file = file + (i * file_delta)
            next_rank = rank + (i * rank_delta)

            if next_file < 1 or next_file > 8 or next_rank < 1 or next_rank > 8:
                break

            next_square = cb.parse_coordinates_to_idx(next_file, next_rank)
            piece_on_board: int = board[next_square]

            if piece_on_board == EMPTY_SQUARE:
                attacked_squares.append(next_square)
                i += 1

            elif (piece_on_board == BLACK_KING and color == WHITE) or (
                piece_on_board == WHITE_KING and color == BLACK
            ):
                attacked_squares.append(next_square)
                i += 1
                continue
                # ennemy king? Add the square behind him
                # next_file = file + (i * file_delta)
                # next_rank = rank + (i * rank_delta)
                # next_square = cb.parse_coordinates_to_idx(next_file, next_rank)
                # attacked_squares.append(next_square)
                # break

            elif (color == WHITE and piece_on_board < 0) or (
                color == BLACK and piece_on_board > 0
            ):
                break

            else:
                attacked_squares.append(next_square)
                break

    return attacked_squares


def generate_queen_moves(board: list[int], square_idx: int, color: int) -> list[int]:
    """
    Generate the list of available squares for a queen.
    Using the 2 functions to generate moves for the rook and the bishop.
    """
    move_list: list[int] = []

    move_list.extend(generate_bishop_moves(board, square_idx, color))
    move_list.extend(generate_rook_moves(board, square_idx, color))

    return move_list


def generate_queen_controlled_squares(
    board: list[int], square_idx: int, color: int
) -> list[int]:
    """ """
    attacked_squares: list[int] = []

    attacked_squares.extend(generate_rook_controlled_squares(board, square_idx, color))
    attacked_squares.extend(
        generate_bishop_controlled_squares(board, square_idx, color)
    )

    return attacked_squares


def generate_king_moves(board: list[int], square_idx: int, color: int) -> list[int]:
    """ """
    file, rank = cb.parse_index(square_idx)

    available_squares: list[int] = []

    directions: list[tuple[int, int]] = [
        (1, 0),
        (0, 1),
        (1, 1),
        (-1, 0),
        (0, -1),
        (-1, 1),
        (1, -1),
        (-1, -1),
    ]

    for file_delta, rank_delta in directions:
        next_file = file + file_delta
        next_rank = rank + rank_delta

        if next_file < 1 or next_file > 8 or next_rank < 1 or next_rank > 8:
            continue

        next_square = cb.parse_coordinates_to_idx(next_file, next_rank)
        piece_on_board = board[next_square]

        if piece_on_board == EMPTY_SQUARE:
            available_squares.append(next_square)

        elif (color == WHITE and piece_on_board < 0) or (
            color == BLACK and piece_on_board > 0
        ):
            available_squares.append(next_square)

        else:
            continue

    return available_squares


def generate_king_controlled_squares(
    board: list[int], square_idx: int, color: int
) -> list[int]:
    """ """
    file, rank = cb.parse_index(square_idx)

    attacked_squares: list[int] = []

    directions: list[tuple[int, int]] = [
        (1, 0),
        (0, 1),
        (1, 1),
        (-1, 0),
        (0, -1),
        (-1, 1),
        (1, -1),
        (-1, -1),
    ]

    for file_delta, rank_delta in directions:
        next_file = file + file_delta
        next_rank = rank + rank_delta

        if next_file < 1 or next_file > 8 or next_rank < 1 or next_rank > 8:
            continue

        next_square = cb.parse_coordinates_to_idx(next_file, next_rank)
        piece_on_board = board[next_square]

        if piece_on_board == EMPTY_SQUARE:
            attacked_squares.append(next_square)

        elif (color == WHITE and piece_on_board < 0) or (
            color == BLACK and piece_on_board > 0
        ):
            continue

        else:
            attacked_squares.append(next_square)

    return attacked_squares


MOVE_GENERATOR = {
    KNIGHT: generate_knight_moves,
    BISHOP: generate_bishop_moves,
    ROOK: generate_rook_moves,
    QUEEN: generate_queen_moves,
}

CONTROLLED_GENERATOR = {
    PAWN: generate_pawn_controlled_squares,
    KNIGHT: generate_knight_controlled_squares,
    BISHOP: generate_bishop_controlled_squares,
    ROOK: generate_rook_controlled_squares,
    QUEEN: generate_queen_controlled_squares,
    KING: generate_king_controlled_squares,
}


def generate_controlled_squares(
    board: list[int], color: int, piece_list: list[int], idx_list: list[int]
) -> set[int]:
    """
    Generate controlled squares for a given color.

    Returns:

    """
    controlled_squares: set[int] = set()

    for piece, idx in zip(piece_list, idx_list):
        controlled_squares.update(CONTROLLED_GENERATOR[abs(piece)](board, idx, color))

    return controlled_squares


def generate_king_legal_moves(
    board: list[int],
    color: int,
    king_square: int,
    ennemy_controlled: set[int],
) -> list[int]:
    """ """
    king_legal_moves: list[int] = []
    king_pseudo_legal = generate_king_moves(board, king_square, color)

    for square_idx in king_pseudo_legal:
        if square_idx not in ennemy_controlled:
            king_legal_moves.append(square_idx)

    return king_legal_moves


def generate_castling_moves(
    board: list[int],
    color: int,
    castling_state: CastlingState,
    ennemy_controlled: set[int],
) -> list[int]:
    """ """
    king_side: bool = castling_state.can_castle_kingside(color)
    queen_side: bool = castling_state.can_castle_queenside(color)

    castling_moves: list[int] = []

    if not (king_side or queen_side):
        return []

    if king_side and is_empty_and_safe_kingside(board, color, ennemy_controlled):
        castling_moves.append(6 if color == WHITE else 62)

    if queen_side and is_empty_and_safe_queenside(board, color, ennemy_controlled):
        castling_moves.append(2 if color == WHITE else 58)

    return castling_moves


def is_empty_and_safe_kingside(
    board: list[int], color: int, ennemy_controlled: set[int]
) -> bool:
    """
    Scan for pieces and verify that squares are safe on the kingside between the king and the rook

    Returns:
        True if no piece is found or none of the squares ares attacked by ennemy pieces
    """
    squares_to_scan: list[int] = [5, 6] if color == WHITE else [61, 62]
    for s in squares_to_scan:
        if board[s] != EMPTY_SQUARE or s in ennemy_controlled:
            return False

    return True


def is_empty_and_safe_queenside(
    board: list[int], color: int, ennemy_controlled: set[int]
) -> bool:
    """
    Scan for pieces on the queenside between the king and the rook

    Returns:
        True if no piece is found
    """
    squares_to_scan: list[int] = [1, 2, 3] if color == WHITE else [57, 58, 59]
    for s in squares_to_scan:
        if board[s] != EMPTY_SQUARE:
            return False
    for s in squares_to_scan[1:]:
        if s in ennemy_controlled:
            return False

    return True


def generate_all_moves(
    board: list[int],
    color: int,
    piece_list: list[int],
    idx_list: list[int],
    king_square: int,
    castling_state: CastlingState,
    ennemy_controlled: set[int],
    en_passant_target: int | None = None,
) -> PieceMoves:
    """ """
    piece_moves = PieceMoves()

    for piece, idx in zip(piece_list, idx_list):
        if abs(piece) == PAWN:
            moves = generate_pawn_moves(board, idx, color, en_passant_target)
        elif abs(piece) == KING:
            moves = generate_king_legal_moves(
                board, color, king_square, ennemy_controlled
            )
            moves.extend(
                generate_castling_moves(board, color, castling_state, ennemy_controlled)
            )
        else:
            moves = MOVE_GENERATOR[abs(piece)](board, idx, color)

        if moves:
            piece_moves.pieces.append(Piece(piece, idx))
            piece_moves.move_list.append(moves)

    return piece_moves


def generate_moves_filter_pinned(
    board: list[int],
    color: int,
    piece_list: list[int],
    idx_list: list[int],
    king_square: int,
    pinned_pieces: list[PinnedPiece],
    castling_state: CastlingState,
    ennemy_controlled: set[int],
    en_passant_target: int | None = None,
) -> PieceMoves:
    """ """
    pin_lookup = {pinned.piece.index: pinned for pinned in pinned_pieces}

    piece_moves = PieceMoves()

    for piece, idx in zip(piece_list, idx_list):
        if abs(piece) == KING:
            moves = generate_king_legal_moves(
                board, color, king_square, ennemy_controlled
            )
            moves.extend(
                generate_castling_moves(board, color, castling_state, ennemy_controlled)
            )
        elif abs(piece) == PAWN:
            moves = generate_pawn_moves(board, idx, color, en_passant_target)
            if idx in pin_lookup:
                moves = filter_pinned_piece_moves(moves, piece, pin_lookup[idx])
        else:
            moves = MOVE_GENERATOR[abs(piece)](board, idx, color)
            if idx in pin_lookup:
                moves = filter_pinned_piece_moves(moves, piece, pin_lookup[idx])

        if moves:
            piece_moves.pieces.append(Piece(piece, idx))
            piece_moves.move_list.append(moves)

    return piece_moves


def filter_pinned_piece_moves(
    moves: list[int], piece: int, pinned_piece: PinnedPiece
) -> list[int]:
    """ """
    pin_vector = pinned_piece.pin_vector
    ennemy_idx = pinned_piece.pinning_piece_index

    filtered_moves: list[int] = []

    if abs(piece) == KNIGHT:
        return []

    elif abs(piece) == ROOK:
        if pin_vector[0] * pin_vector[1] != 0:
            return []
        else:
            for move in moves:
                if cb.is_index_aligned(move, ennemy_idx):
                    filtered_moves.append(move)

    elif abs(piece) == BISHOP:
        if pin_vector[0] * pin_vector[1] == 0:
            return []
        else:
            for move in moves:
                if cb.is_index_on_diagonal(move, ennemy_idx):
                    filtered_moves.append(move)

    elif abs(piece) in [QUEEN, PAWN]:
        if pin_vector[0] * pin_vector[1] == 0:
            for move in moves:
                if cb.is_index_aligned(move, ennemy_idx):
                    filtered_moves.append(move)
        else:
            for move in moves:
                if cb.is_index_on_diagonal(move, ennemy_idx):
                    filtered_moves.append(move)

    return filtered_moves


def generate_single_check_moves(
    board: list[int],
    color: int,
    piece_list: list[int],
    idx_list: list[int],
    king_square: int,
    checking_piece: Piece,
    pinned_pieces: list[PinnedPiece],
    ennemy_controlled: set[int],
    en_passant_target: int | None = None,
) -> PieceMoves:
    """ """
    allowed_squares: set[int] = set()

    capturing_move = checking_piece.index

    if abs(checking_piece.piece) in [KNIGHT, PAWN]:
        allowed_squares.add(capturing_move)

    else:
        allowed_squares.add(capturing_move)
        allowed_squares.update(
            generate_blocking_moves(board, king_square, checking_piece)
        )

    if pinned_pieces == []:
        return generate_single_check_no_pin_moves(
            board,
            color,
            piece_list,
            idx_list,
            king_square,
            ennemy_controlled,
            allowed_squares,
            en_passant_target,
        )

    else:
        return generate_single_check_pinned_moves(
            board,
            color,
            piece_list,
            idx_list,
            king_square,
            pinned_pieces,
            ennemy_controlled,
            allowed_squares,
            en_passant_target,
        )


def generate_single_check_no_pin_moves(
    board: list[int],
    color: int,
    piece_list: list[int],
    idx_list: list[int],
    king_square: int,
    ennemy_controlled: set[int],
    allowed_squares: set[int],
    en_passant_target: int | None = None,
) -> PieceMoves:
    piece_moves = PieceMoves()

    for piece, idx in zip(piece_list, idx_list):
        legal_moves: list[int] = []
        if abs(piece) == KING:
            moves = generate_king_legal_moves(
                board, color, king_square, ennemy_controlled
            )
            piece_moves.pieces.append(Piece(piece, idx))
            piece_moves.move_list.append(moves)
            continue

        elif abs(piece) == PAWN:
            moves = generate_pawn_moves(board, idx, color, en_passant_target)

        else:
            moves = MOVE_GENERATOR[abs(piece)](board, idx, color)

        for move in moves:
            if move in allowed_squares:
                legal_moves.append(move)

        if legal_moves:
            piece_moves.pieces.append(Piece(piece, idx))
            piece_moves.move_list.append(legal_moves)

    return piece_moves


def generate_single_check_pinned_moves(
    board: list[int],
    color: int,
    piece_list: list[int],
    idx_list: list[int],
    king_square: int,
    pinned_pieces: list[PinnedPiece],
    ennemy_controlled: set[int],
    allowed_squares: set[int],
    en_passant_target: int | None = None,
) -> PieceMoves:
    pin_lookup = {pinned.piece.index: pinned for pinned in pinned_pieces}

    piece_moves = PieceMoves()

    for piece, idx in zip(piece_list, idx_list):
        legal_moves: list[int] = []
        if abs(piece) == KING:
            moves = generate_king_legal_moves(
                board, color, king_square, ennemy_controlled
            )
            piece_moves.pieces.append(Piece(piece, idx))
            piece_moves.move_list.append(moves)
            continue

        elif abs(piece) == PAWN:
            moves = generate_pawn_moves(board, idx, color, en_passant_target)
            if idx in pin_lookup:
                moves = filter_pinned_piece_moves(moves, piece, pin_lookup[idx])

        else:
            moves = MOVE_GENERATOR[abs(piece)](board, idx, color)
            if idx in pin_lookup:
                moves = filter_pinned_piece_moves(moves, piece, pin_lookup[idx])

        for move in moves:
            if move in allowed_squares:
                legal_moves.append(move)

        if legal_moves:
            piece_moves.pieces.append(Piece(piece, idx))
            piece_moves.move_list.append(legal_moves)

    return piece_moves


def generate_blocking_moves(
    board: list[int], king_square: int, checking_piece: Piece
) -> list[int]:
    """ """

    blocking_moves: list[int] = []

    k_file, k_rank = cb.parse_index(king_square)
    c_file, c_rank = cb.parse_index(checking_piece.index)

    file_diff = k_file - c_file
    rank_diff = k_rank - c_rank

    f_delta = file_diff if file_diff == 0 else (1 if file_diff > 0 else -1)
    r_delta = rank_diff if rank_diff == 0 else (1 if rank_diff > 0 else -1)

    i = 1
    while True:
        new_file = c_file + (i * f_delta)
        new_rank = c_rank + (i * r_delta)

        if new_file < 1 or new_file > 8 or new_rank < 1 or new_rank > 8:
            break

        square = cb.parse_coordinates_to_idx(new_file, new_rank)
        if abs(board[square]) == KING:
            return blocking_moves
        blocking_moves.append(square)
        i += 1

    return blocking_moves


if __name__ == "__main__":
    b = cb.create_starting_position()
