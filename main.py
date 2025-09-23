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

    ##########################################
    # ------ 2 OR MORE CHECKING PIECE ------ #
    ##########################################

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

    ###################################
    # ------ NO CHECKING PIECE ------ #
    ###################################

    # no checking piece? generate all moves

    elif not checking_pieces:
        # If no pinned pieces we generate all the moves without filtering
        if not pinned_pieces:
            return mv.generate_all_moves(
                board,
                color,
                piece_list,
                idx_list,
                king_square,
                castling_state,
                ennemy_controlled,
                en_passant_target,
            )

        # If there is pinned pieces we filter as we generate the moves
        else:
            return mv.generate_moves_filter_pinned(
                board,
                color,
                piece_list,
                idx_list,
                king_square,
                pinned_pieces,
                ennemy_controlled,
                en_passant_target,
            )

    ##################################
    # ------ 1 CHECKING PIECE ------ #
    ##################################

    # 1 checking piece? legal king moves + blocking moves

    else:
        return mv.generate_single_check_moves(...)


def find_blocking_moves(
    board: list[int], checking_piece: tuple[int, int], king_square_idx: int, color: int
) -> config.PieceMoves: ...
def filter_pinned_pieces(piece_moves: config.PieceMoves) -> config.PieceMoves: ...


def find_best_move(board: list[int], color: int) -> list[int]:
    gl.analyze_king_safety()
    best_move = evaluate_minmax(board, move_list, color)

    new_board = make_move(board, best_move)

    return new_board


if __name__ == "__main__":
    main()
