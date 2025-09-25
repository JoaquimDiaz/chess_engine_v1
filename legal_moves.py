# from game_state import GameState
import move_generation as mv
import game_logic as gl
import logging

from chess_board import ChessBoard, BoardState, create_starting_position
from config import BLACK, WHITE, CastlingState, Piece, PieceMoves, PinnedPiece

logger = logging.getLogger(__name__)


def generate_legal_moves(
    # game_state: GameState,
    board: list[int],
    color: int,
    board_state: BoardState,
    checking_pieces: list[Piece],
    pinned_pieces: list[PinnedPiece],
    castling_state: CastlingState,
    en_passant_target: int | None = None,
) -> PieceMoves:
    """ """
    # board = game_state.board
    # color = game_state.active_color
    # board_state = game_state.board_state
    # castling_state = game_state.castling_state
    # en_passant_target = game_state.en_passant_target
    # Get piece informations
    piece_list, idx_list, king_square = board_state.get_color_state(color)

    # Get ennemy piece information
    ennemy_color = BLACK if color == WHITE else WHITE

    e_piece_list, e_idx_list, _ = board_state.get_color_state(ennemy_color)

    # Get king safety informations

    ennemy_controlled: set[int] = mv.generate_controlled_squares(
        board, ennemy_color, e_piece_list, e_idx_list
    )

    ##########################################
    # ------ 2 OR MORE CHECKING PIECE ------ #
    ##########################################

    # more than 1 checking piece? king as to move
    # - We return only the king legal moves

    if checking_pieces and len(checking_pieces) > 1:
        legal_moves = mv.generate_king_legal_moves(
            board, color, king_square, ennemy_controlled
        )
        if legal_moves == []:
            return PieceMoves()
        else:
            return PieceMoves(
                pieces=[Piece(board[king_square], king_square)], move_list=[legal_moves]
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
                castling_state,
                ennemy_controlled,
                en_passant_target,
            )

    ##################################
    # ------ 1 CHECKING PIECE ------ #
    ##################################

    # 1 checking piece? legal king moves + blocking moves

    else:
        return mv.generate_single_check_moves(
            board,
            color,
            piece_list,
            idx_list,
            king_square,
            checking_pieces[0],
            pinned_pieces,
            ennemy_controlled,
            en_passant_target,
        )
