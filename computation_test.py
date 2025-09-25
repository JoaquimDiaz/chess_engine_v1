import time

from game_state import GameState
from legal_moves import generate_legal_moves


def time_move_generation(iterations: int):
    g = GameState.starting_position()

    start_time = time.time()
    for i in range(iterations):
        _ = generate_legal_moves(g)
    end_time = time.time()

    total_time = end_time - start_time

    print(f"Number of iterations: {iterations}")
    print(f"Total time: {total_time}")
    print(f"Average time per call: {total_time / iterations}")


if __name__ == "__main__":
    time_move_generation(10_000)
