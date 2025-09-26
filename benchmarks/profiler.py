import cProfile
import time
import pstats

from game_state import GameState
from move_selection import minmax_selection


def profile_engine(fen: str, depth: int = 3):
    """Profile your engine on a specific position"""
    pr = cProfile.Profile()
    pr.enable()

    # Run your engine
    game_state = GameState.from_fen(fen)
    move = minmax_selection(game_state, depth)

    pr.disable()
    stats = pstats.Stats(pr)
    stats.sort_stats("cumulative").print_stats(20)

    return move


if __name__ == "__main__":
    ...
