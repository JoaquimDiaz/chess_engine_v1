import chess_board as cb
from chess_board import BoardState, ChessBoard
import move_generation as mv
import pytest

from config import (
    EMPTY_SQUARE,
    WHITE,
    BLACK,
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
)


def sq(square: str) -> int:
    """Quick helper for tests: sq('a1') return index 0"""
    return cb.square_to_index(square)


def assert_move_set_equality(moves: list[int], expected_moves: list[int | str]) -> None:
    moves2: list[int] = []
    for square in expected_moves:
        if isinstance(square, str):
            moves2.append(cb.square_to_index(square))
        else:
            moves2.append(square)
    assert set(moves) == set(moves2)


def test_pawn_move():
    b = ChessBoard(True)

    moves = mv.generate_pawn_moves(b.board, sq("a2"), WHITE)
    assert_move_set_equality(moves, [16, 24])

    moves = mv.generate_pawn_moves(b.board, 15, WHITE)
    assert_move_set_equality(moves, [23, 31])

    moves = mv.generate_pawn_moves(b.board, 50, BLACK)
    assert_move_set_equality(moves, [42, 34])

    moves = mv.generate_pawn_moves(b.board, 48, BLACK)
    assert_move_set_equality(moves, [40, 32])

    b.make_move("a2", "a4")
    b.make_move("b7", "b5")

    moves = mv.generate_pawn_moves(b.board, 24, WHITE)
    assert_move_set_equality(moves, [32, 33])

    b.make_move("c2", "c6")

    moves = mv.generate_pawn_moves(b.board, 33, BLACK)
    assert_move_set_equality(moves, [25, 24])

    b = ChessBoard()
    b["g7"] = WHITE_PAWN
    b["h8"] = BLACK_ROOK

    moves = mv.generate_pawn_moves(b.board, 54, WHITE)
    assert_move_set_equality(moves, [62, 63])


def test_pawn_controll():
    b = ChessBoard(True)

    control = mv.generate_pawn_controlled_squares(b.board, 10, WHITE)
    assert_move_set_equality(control, [17, 19])

    control = mv.generate_pawn_controlled_squares(b.board, 53, BLACK)
    assert_move_set_equality(control, [44, 46])

    b = ChessBoard()
    b[8] = BLACK_PAWN

    control = mv.generate_pawn_controlled_squares(b.board, 8, BLACK)
    assert_move_set_equality(control, [1])


def test_knight_move():
    b = ChessBoard(True)

    moves = mv.generate_knight_moves(b.board, 6, WHITE)
    assert_move_set_equality(moves, ["f3", "h3"])

    moves = mv.generate_knight_moves(b.board, 57, BLACK)
    assert_move_set_equality(moves, ["a6", "c6"])

    b.make_move("e2", "e4")
    b.make_move("e7", "e5")
    b.make_move("g1", "f3")

    moves = mv.generate_knight_moves(b.board, 21, WHITE)
    assert_move_set_equality(moves, ["d4", "e5", "g5", "h4", "g1"])

    b.make_move("b8", "c6")

    moves = mv.generate_knight_moves(b.board, sq("c6"), BLACK)
    assert_move_set_equality(moves, ["e7", "d4", "b4", "b8", "a5"])


def test_kngiht_controll():
    b = ChessBoard(True)

    control = mv.generate_knight_controlled_squares(b.board, sq("b1"), WHITE)
    assert_move_set_equality(control, ["a3", "c3", "d2"])

    b.make_move("b8", "c3")

    control = mv.generate_knight_controlled_squares(b.board, sq("c3"), BLACK)
    assert_move_set_equality(control, ["a4", "b5", "d5", "e4"])


def test_rook_move():
    b = ChessBoard(True)

    moves = mv.generate_rook_moves(b.board, sq("a1"), WHITE)
    assert moves == []

    b["a2"] = EMPTY_SQUARE

    moves = mv.generate_rook_moves(b.board, sq("a1"), WHITE)
    assert_move_set_equality(moves, ["a2", "a3", "a4", "a5", "a6", "a7"])

    b["a4"] = BLACK_ROOK

    moves = mv.generate_rook_moves(b.board, sq("a4"), BLACK)
    assert_move_set_equality(
        moves, ["a1", "a2", "a3", "a5", "a6", "b4", "c4", "d4", "e4", "f4", "g4", "h4"]
    )


def test_rook_controll():
    b = ChessBoard(True)

    control = mv.generate_rook_controlled_squares(b.board, sq("a1"), WHITE)
    assert_move_set_equality(control, ["a2", "b1"])

    b["e4"] = BLACK_ROOK

    control = mv.generate_rook_controlled_squares(b.board, sq("e4"), BLACK)
    assert_move_set_equality(
        control, ["e3", "e5", "e6", "e7", "f4", "g4", "h4", "d4", "c4", "b4", "a4"]
    )


def test_bishop_move():
    b = ChessBoard(True)

    moves = mv.generate_bishop_moves(b.board, sq("c1"), WHITE)
    assert moves == []

    b.make_move("d2", "d4")

    b["h6"] = BLACK_PAWN

    moves = mv.generate_bishop_moves(b.board, sq("c1"), WHITE)
    assert_move_set_equality(moves, ["d2", "e3", "f4", "g5", "h6"])

    b["a3"] = BLACK_BISHOP

    moves = mv.generate_bishop_moves(b.board, sq("a3"), BLACK)
    assert_move_set_equality(moves, ["b4", "c5", "d6", "b2"])


def test_bishop_controll():
    b = ChessBoard(True)

    control = mv.generate_bishop_controlled_squares(b.board, sq("c1"), WHITE)
    assert_move_set_equality(control, ["b2", "d2"])

    b.make_move("b2", "b4")

    control = mv.generate_bishop_controlled_squares(b.board, sq("c1"), WHITE)
    assert_move_set_equality(control, ["b2", "d2", "a3"])

    b["h5"] = BLACK_BISHOP

    control = mv.generate_bishop_controlled_squares(b.board, sq("h5"), BLACK)
    assert_move_set_equality(control, ["g4", "f3", "g6", "f7"])


def test_queen_moves():
    b = ChessBoard(True)

    moves = mv.generate_queen_moves(b.board, sq("d1"), WHITE)
    assert moves == []

    b["e4"] = WHITE_QUEEN

    moves = mv.generate_queen_moves(b.board, sq("e4"), WHITE)
    expected_moves: list[int | str] = [
        "f3",
        "f4",
        "g4",
        "h4",
        "d4",
        "c4",
        "b4",
        "a4",
        "e5",
        "e6",
        "e7",
        "d5",
        "c6",
        "b7",
        "d3",
        "e3",
        "f5",
        "g6",
        "h7",
    ]
    assert_move_set_equality(moves, expected_moves)

    b["d4"] = WHITE_QUEEN
    b["d7"] = EMPTY_SQUARE

    moves = mv.generate_queen_moves(b.board, sq("d8"), BLACK)
    assert_move_set_equality(moves, ["d7", "d6", "d5", "d4"])


def test_queen_controll():
    b = ChessBoard(True)

    control = mv.generate_queen_controlled_squares(b.board, sq("d1"), WHITE)
    assert_move_set_equality(control, ["e1", "c1", "c2", "e2", "d2"])

    b["d5"] = BLACK_QUEEN

    control = mv.generate_queen_controlled_squares(b.board, sq("d5"), BLACK)
    assert_move_set_equality(
        control,
        [
            "c6",
            "b7",
            "c5",
            "b5",
            "a5",
            "e5",
            "f5",
            "g5",
            "h5",
            "e6",
            "f7",
            "e4",
            "f3",
            "d7",
            "d6",
            "d4",
            "d3",
            "c4",
            "b3",
        ],
    )


def test_generate_king_controll():
    b = ChessBoard(True)

    control = mv.generate_king_controlled_squares(b.board, sq("e1"), WHITE)
    assert_move_set_equality(control, ["d1", "d2", "e2", "f2", "f1"])

    b["f3"] = BLACK_KING

    control = mv.generate_king_controlled_squares(b.board, sq("f3"), BLACK)
    assert_move_set_equality(control, ["e3", "e4", "f4", "g4", "g3"])


def test_generate_king_legal_moves():
    b = ChessBoard(True)

    ennemy_controlled = mv.generate_controlled_squares(
        b.board, BLACK, b.b_pieces, b.b_idx
    )
    moves = mv.generate_king_legal_moves(
        b.board, WHITE, b.w_king_idx, ennemy_controlled
    )

    assert moves == []

    b.make_move("e2", "e4")
    b.make_move("f2", "f4")
    b.make_move("g2", "g4")
    b["h4"] = BLACK_QUEEN

    ennemy_controlled = mv.generate_controlled_squares(
        b.board, BLACK, b.b_pieces, b.b_idx
    )
    moves = mv.generate_king_legal_moves(
        b.board, WHITE, b.w_king_idx, ennemy_controlled
    )

    assert_move_set_equality(moves, ["e2"])
