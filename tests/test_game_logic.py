import chess_board as cb
from chess_board import ChessBoard, parse_index
import move_generation as mv
import game_logic as gl
import config
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
import pytest


def sq(square: str) -> int:
    """Quick helper for tests: sq('a1') return index 0"""
    return cb.square_to_index(square)


b = ChessBoard()

b[0] = BLACK_BISHOP
b[62] = BLACK_ROOK
b[6] = BLACK_ROOK
b[54] = WHITE_KING
b[5] = BLACK_KING


def test_diagonal_checks():
    file, rank = cb.parse_index(b.w_king_idx)
    checking_piece, pinned_piece = gl.directional_check(
        b.board, file, rank, WHITE, (-1, -1)
    )
    assert pinned_piece is None
    assert checking_piece is not None
    assert checking_piece == Piece(BLACK_BISHOP, sq("a1"))


def test_diagonal_pin():
    b2 = b.copy()
    b2["c3"] = WHITE_QUEEN
    file, rank = cb.parse_index(b2.w_king_idx)
    checking_piece, pinned_piece = gl.directional_check(
        b2.board, file, rank, WHITE, (-1, -1)
    )

    assert checking_piece is None
    assert pinned_piece is not None
    assert pinned_piece.piece == Piece(WHITE_QUEEN, sq("c3"))


def test_aligned_checks():
    b3 = b.copy()

    file, rank = cb.parse_index(b3.w_king_idx)
    checking_piece, pinned_piece = gl.directional_check(
        b3.board, file, rank, WHITE, (0, 1)
    )
    assert pinned_piece is None
    assert checking_piece is not None
    assert checking_piece == Piece(BLACK_ROOK, sq("g8"))

    checking_piece, pinned_piece = gl.directional_check(
        b3.board, file, rank, WHITE, (0, -1)
    )
    assert pinned_piece is None
    assert checking_piece is not None
    assert checking_piece == Piece(BLACK_ROOK, sq("g1"))


def test_aligned_pin():
    b4 = b.copy()
    b4["g2"] = WHITE_QUEEN

    file, rank = cb.parse_index(b4.w_king_idx)
    checking_piece, pinned_piece = gl.directional_check(
        b4.board, file, rank, WHITE, (0, -1)
    )

    assert checking_piece is None
    assert pinned_piece is not None
    assert pinned_piece.piece == Piece(WHITE_QUEEN, sq("g2"))


def test_knight_check():
    b = ChessBoard()
    b["c1"] = BLACK_KING
    b["a2"] = WHITE_KNIGHT

    file, rank = cb.parse_index(b.b_king_idx)
    result = gl.knight_check(b.board, file, rank, BLACK)

    assert result is not None
    assert result == Piece(WHITE_KNIGHT, sq("a2"))


def test_analyze_king_safety():
    b = ChessBoard()
    with pytest.raises(ValueError):
        gl.analyze_king_safety(b.board, sq("a1"), BLACK)

    b["a1"] = WHITE_KING
    b["a8"] = BLACK_KING
    b["h8"] = BLACK_BISHOP

    checking_pieces, pinned_pieces = gl.analyze_king_safety(
        b.board, b.w_king_idx, WHITE
    )

    assert pinned_pieces == []
    assert checking_pieces != []
    assert len(checking_pieces) == 1

    assert checking_pieces[0] == Piece(BLACK_BISHOP, sq("h8"))
