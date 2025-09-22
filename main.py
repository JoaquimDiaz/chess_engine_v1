import chess_board as cb
import move_generation as mv
import game_logic as gl
import config
import logging

from config import BLACK, WHITE, CastlingState, Piece, PieceMoves

logger = logging.getLogger(__name__)


def main():
    board = cb.create_starting_position()
    castling_state = config.CastlingState()

    board = find_best_move(board, config.WHITE, castling_state)


def generate_legal_moves(
    board: list[int],
    color: int,
    board_state: cb.BoardState,
    castling_state: CastlingState,
    en_passant_target: int | None = None,
) -> PieceMoves:
    """ """
    # Get piece informations
    piece_list, idx_list, king_square = board_state.get_color_state(color)

    # Get ennemy piece information
    ennemy_color = BLACK if color == WHITE else WHITE

    e_piece_list, e_idx_list, _ = board_state.get_color_state(ennemy_color)

    # Get king safety informations
    checking_pieces, pinned_pieces = gl.analyze_king_safety(board, king_square, color)

    ennemy_controlled: set[int] = mv.generate_controlled_squares(
        board, ennemy_color, e_piece_list, e_idx_list
    )

    # ------ 1 OR MORE CHECKING PIECE ------ #
    # more than 1 checking piece? king as to move
    # - We return only the king legal moves
    if checking_pieces and len(checking_pieces) > 1:
        return PieceMoves(
            pieces=[Piece(board[king_square], king_square)],
            move_list=[
                mv.generate_king_legal_moves(
                    board, color, king_square, ennemy_controlled
                )
            ],
        )

    # ------ NO CHECKING PIECE ------ #
    # no checking piece? generate all moves
    elif not checking_pieces:
        # If no pinned pieces we generate all the moves without filtering
        if not pinned_pieces:
            return mv.generate_all_moves(
                board, color, board_state, castling_state, en_passant_target
            )

        # If there is pinned pieces we filter as we generate the moves
        else:
            return mv.generate_moves_filter_pinned(...)

    # ------ 1 CHECKING PIECE ------ #
    # 1 checking piece? legal king moves + blocking moves
    else:
        return mv.generate_single_check_moves(...)


def find_blocking_moves(
    board: list[int], checking_piece: tuple[int, int], king_square_idx: int, color: int
) -> config.PieceMoves: ...
def filter_pinned_pieces(piece_moves: config.PieceMoves) -> config.PieceMoves: ...


def generate_legal_moves(board: list[int], color: Literal[1, 0]) -> list[str]:
    # List of candidate move
    move_list: list[str] = []

    # Tuple with pieces position on the board
    board_state = cb.find_pieces(board)

    # 2 Lists with checking and pinned pieces in the position
    if color == config.WHITE:
        checking_pieces, pinned_pieces = gl.analyze_king_safety(board, board_state[4])
    elif color == config.BLACK:
        checking_pieces, pinned_pieces = gl.analyze_king_safety(board, board_state[5])

    if len(checking_pieces) > 1:
        return mv.generate_king_legal_moves(board, board_state, color)

    # Generating the list of all available moves ignoring legality
    move_list.extend(mv.generate_all_moves(board, board_state, pinned_pieces, color))

    if len(checking_pieces) == 1:
        move_list = filter_legal_moves(board, board_state, pinned_pieces, color)

    return move_list


def find_best_move(board: list[int], color: int) -> list[int]:
    gl.analyze_king_safety()
    best_move = evaluate_minmax(board, move_list, color)

    new_board = make_move(board, best_move)

    return new_board


if __name__ == "__main__":
    main()
