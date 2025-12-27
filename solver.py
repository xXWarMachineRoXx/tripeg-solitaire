from collections import deque

# Colors
RED = (200, 60, 60)
GREEN = (60, 180, 60)

# Initial peg colors
START = {
    1: RED,
    2: RED,
    3: GREEN,
    4: GREEN,
    5: RED,
    6: RED,
    7: GREEN,
    8: GREEN,
    9: RED,
    10: GREEN,
    11: RED,
    12: GREEN,
}

# Ring definitions
RING_A = [1, 2, 6, 9, 8, 4]
RING_B = [2, 3, 7, 10, 9, 5]
RING_C = [5, 6, 10, 12, 11, 8]

MOVES = {
    "A_cw": (RING_A, True),
    "A_ccw": (RING_A, False),
    "B_cw": (RING_B, True),
    "B_ccw": (RING_B, False),
    "C_cw": (RING_C, True),
    "C_ccw": (RING_C, False),
}
INNER_TRIANGLE = {2, 6, 10, 9, 8, 5}


def rotate(state: dict[int, tuple[int, int, int]], cycle: list[int], clockwise: bool) -> dict[int, tuple[int, int, int]]:
    vals = [state[i] for i in cycle]
    vals = vals[-1:] + vals[:-1] if clockwise else vals[1:] + vals[:1]
    out = state.copy()
    for i, v in zip(cycle, vals):
        out[i] = v
    return out


def serialize(state: dict[int, tuple[int, int, int]]) -> tuple:
    return tuple(state[i] for i in sorted(state))


def is_goal(state: dict[int, tuple[int, int, int]]) -> bool:
    """Goal: all inner triangle positions are GREEN."""
    return all(state[i] == GREEN for i in INNER_TRIANGLE)


def solve_full_bfs():
    """Exhaustively search all reachable states; returns shortest solution or None."""
    start_key = serialize(START)
    if is_goal(START):
        return []

    q = deque([(start_key, START, [])])
    seen = {start_key}

    while q:
        key, state, path = q.popleft()
        if is_goal(state):
            return path
        for name, (cycle, cw) in MOVES.items():
            nxt = rotate(state, cycle, cw)
            nkey = serialize(nxt)
            if nkey in seen:
                continue
            seen.add(nkey)
            q.append((nkey, nxt, path + [name]))
    return None


if __name__ == "__main__":
    solution = solve_full_bfs()
    if solution is None:
        print("Goal (all green) is unreachable from this start state.")
    else:
        print("Solution (" + str(len(solution)) + " moves):", " -> ".join(solution))
