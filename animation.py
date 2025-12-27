import sys
import math
import time
import pygame
from collections import deque

pygame.init()

# Window
WIDTH, HEIGHT = 800, 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Triangular Peg Animation")
FONT = pygame.font.SysFont(None, 28)
TITLE_FONT = pygame.font.SysFont(None, 34)

# Colors
WHITE = (240, 240, 240)
BLACK = (20, 20, 20)
RED = (200, 60, 60)
GREEN = (60, 180, 60)
GRAY = (120, 120, 120)
YELLOW = (255, 200, 0)

RADIUS = 18

# Board layout
ROW_LENGTHS = [3, 4, 3, 2]
H_SPACING = 110
V_SPACING = H_SPACING * math.sqrt(3) / 2


def build_layout():
    nodes = {}
    coords = {}
    idx = 1
    y0 = 140
    for r, length in enumerate(ROW_LENGTHS):
        y = y0 + r * V_SPACING
        x_start = WIDTH / 2 - (length - 1) * H_SPACING / 2
        for c in range(length):
            x = x_start + c * H_SPACING
            nodes[idx] = (x, y)
            coords[(r, c)] = idx
            idx += 1
    return nodes, coords


DIRS = [(0, 1), (1, 0), (1, 1)]


def build_edges(coords):
    edges = set()
    for (r, c), a in coords.items():
        for dr, dc in DIRS:
            b = coords.get((r + dr, c + dc))
            if b:
                edges.add(tuple(sorted((a, b))))
    remove_edges = {(4, 9), (5, 10), (8, 12)}
    add_edges = {(5, 8), (7, 10), (10, 12), (9, 11), (6, 9)}
    edges = {tuple(sorted(e)) for e in edges}
    edges -= {tuple(sorted(e)) for e in remove_edges}
    edges |= {tuple(sorted(e)) for e in add_edges}
    return sorted(edges)


NODES, COORDS = build_layout()
EDGES = build_edges(COORDS)
ROW_NODES = []
idx = 1
for length in ROW_LENGTHS:
    ROW_NODES.append([idx + i for i in range(length)])
    idx += length

# Rings
RING_A = [1, 2, 6, 9, 8, 4]
RING_B = [2, 3, 7, 10, 9, 5]
RING_C = [5, 6, 10, 12, 11, 8]

# Goal (updated inner triangle)
INNER_TRIANGLE = {2, 6, 10, 9, 8, 5}

# Start state
START_COLORS = {
    1: RED,
    2: GREEN,
    3: RED,
    4: GREEN,
    5: RED,
    6: GREEN,
    7: GREEN,
    8: RED,
    9: GREEN,
    10: RED,
    11: GREEN,
    12: RED,
}


def rotate(state, cycle, cw):
    vals = [state[i] for i in cycle]
    vals = vals[-1:] + vals[:-1] if cw else vals[1:] + vals[:1]
    out = state.copy()
    for i, v in zip(cycle, vals):
        out[i] = v
    return out


def serialize(state):
    return tuple(state[i] for i in sorted(state))


def is_goal(state):
    return all(state[i] == GREEN for i in INNER_TRIANGLE)


MOVES = {
    "A_cw": (RING_A, True),
    "A_ccw": (RING_A, False),
    "B_cw": (RING_B, True),
    "B_ccw": (RING_B, False),
    "C_cw": (RING_C, True),
    "C_ccw": (RING_C, False),
}

def move_label(name):
    ring, direction = name.split("_", 1)
    dir_text = "clockwise" if direction == "cw" else "counter-clockwise"
    return f"Ring {ring} {dir_text}"


def solve_full_bfs():
    start_key = serialize(START_COLORS)
    if is_goal(START_COLORS):
        return []
    q = deque([(start_key, START_COLORS, [])])
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


def draw_state(state, step_text="", highlight=None):
    SCREEN.fill(WHITE)
    title = TITLE_FONT.render("Triangular Peg Animation", True, BLACK)
    SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))
    if step_text:
        info = FONT.render(step_text, True, BLACK)
        SCREEN.blit(info, (WIDTH // 2 - info.get_width() // 2, 60))
    # Edges
    for a, b in EDGES:
        ax, ay = NODES[a]
        bx, by = NODES[b]
        pygame.draw.line(SCREEN, GRAY, (int(ax), int(ay)), (int(bx), int(by)), 3)
    # Nodes
    highlight = set(highlight or [])

    for i, (x, y) in NODES.items():
        color = state.get(i)
        if i in highlight:
            pygame.draw.circle(SCREEN, YELLOW, (int(x), int(y)), RADIUS + 5, 4)
        if color is not None:
            pygame.draw.circle(SCREEN, color, (int(x), int(y)), RADIUS)
        else:
            pygame.draw.circle(SCREEN, GRAY, (int(x), int(y)), RADIUS, 2)
        # labels
        label = FONT.render(str(i), True, BLACK)
        SCREEN.blit(label, (int(x) - 6, int(y) - 28))
    # Goal banner
    if is_goal(state):
        win_text = TITLE_FONT.render("YOU WIN!", True, GREEN)
        SCREEN.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()


def animate(sequence, delay=1.2):
    state_history = [START_COLORS.copy()]
    step_idx = 0
    auto_play = False
    auto_acc = 0.0
    highlight = None
    steps_text = [f"{i + 1}. {move_label(m)}" for i, m in enumerate(sequence)]

    button_defs = {
        "Prev": pygame.Rect(30, HEIGHT - 70, 100, 40),
        "Next": pygame.Rect(150, HEIGHT - 70, 100, 40),
        "Play": pygame.Rect(270, HEIGHT - 70, 120, 40),
    }

    clock = pygame.time.Clock()

    def draw_ui():
        step_text = f"Step {step_idx}/{len(sequence)}"
        if auto_play:
            step_text += "  (auto)"
        draw_state(state_history[step_idx], step_text, highlight=highlight)
        for name, rect in button_defs.items():
            if name == "Play":
                bg = GREEN if auto_play else GRAY
                txt = "Pause" if auto_play else "Play"
                pygame.draw.rect(SCREEN, bg, rect, border_radius=6)
                label = FONT.render(txt, True, BLACK)
            else:
                pygame.draw.rect(SCREEN, GRAY, rect, border_radius=6)
                label = FONT.render(name, True, BLACK)
            SCREEN.blit(label, (rect.x + (rect.width - label.get_width()) // 2, rect.y + 10))
        # Step list
        panel_x = WIDTH - 240
        panel_y = 120
        header = TITLE_FONT.render("Steps", True, BLACK)
        SCREEN.blit(header, (panel_x, panel_y))
        panel_y += 40
        for i, text in enumerate(steps_text):
            if i < step_idx:
                color = GRAY
                prefix = "✓ "
            elif i == step_idx:
                color = GREEN
                prefix = "> "
            else:
                color = BLACK
                prefix = "  "
            line = FONT.render(prefix + text, True, color)
            SCREEN.blit(line, (panel_x, panel_y))
            panel_y += 24
        pygame.display.flip()

    draw_ui()

    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_r:
                    return True  # replay
                if event.key == pygame.K_RIGHT:
                    # Next
                    if step_idx < len(sequence):
                        move = sequence[step_idx]
                        cycle, cw = MOVES[move]
                        new_state = rotate(state_history[step_idx], cycle, cw)
                        state_history.append(new_state)
                        step_idx += 1
                        highlight = cycle
                        draw_ui()
                if event.key == pygame.K_LEFT:
                    # Prev
                    if step_idx > 0:
                        state_history.pop()
                        step_idx -= 1
                        highlight = sequence[step_idx - 1] if step_idx > 0 else None
                        if highlight:
                            highlight = MOVES[highlight][0]
                        draw_ui()
                if event.key == pygame.K_SPACE:
                    auto_play = not auto_play
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                if button_defs["Prev"].collidepoint(pos):
                    if step_idx > 0:
                        state_history.pop()
                        step_idx -= 1
                        highlight = sequence[step_idx - 1] if step_idx > 0 else None
                        if highlight:
                            highlight = MOVES[highlight][0]
                        draw_ui()
                elif button_defs["Next"].collidepoint(pos):
                    if step_idx < len(sequence):
                        move = sequence[step_idx]
                        cycle, cw = MOVES[move]
                        new_state = rotate(state_history[step_idx], cycle, cw)
                        state_history.append(new_state)
                        step_idx += 1
                        highlight = cycle
                        draw_ui()
                elif button_defs["Play"].collidepoint(pos):
                    auto_play = not auto_play

        if auto_play and step_idx < len(sequence):
            auto_acc += dt
            if auto_acc >= delay:
                auto_acc = 0.0
                move = sequence[step_idx]
                cycle, cw = MOVES[move]
                new_state = rotate(state_history[step_idx], cycle, cw)
                state_history.append(new_state)
                step_idx += 1
                highlight = cycle
                draw_ui()
        elif auto_play and step_idx >= len(sequence):
            auto_play = False

        # Small sleep to avoid busy loop
        pygame.time.delay(10)

    return False


def main():
    seq = solve_full_bfs()
    if seq is None:
        print("No solution found.")
        return
    print("Solution (" + str(len(seq)) + " moves):", " -> ".join(seq))
    replay = True
    while replay:
        replay = animate(seq)
    pygame.quit()


if __name__ == "__main__":
    main()
