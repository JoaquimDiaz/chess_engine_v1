from config import EMPTY_SQUARE, PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING, WHITE

EVAL_DICT = {PAWN: 1, KNIGHT: 3, BISHOP: 3, ROOK: 5, QUEEN: 9, KING: 0}


def evaluate_position(
    active_color: int,
    w_piece_list: list[int],
    b_piece_list: list[int],
    checkmate: bool,
    draw: bool,
) -> float:
    if draw:
        return 0
    elif checkmate:
        return -10_000 if active_color == WHITE else +10_000
    else:
        w_score: int = 0
        b_score: int = 0

        for piece in w_piece_list:
            w_score += EVAL_DICT[abs(piece)]
        for piece in b_piece_list:
            b_score += EVAL_DICT[abs(piece)]

        return w_score - b_score


if __name__ == "__main__":
    ...
