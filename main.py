import sys
import math
from collections import deque
import pygame

pygame.init()

WIDTH, HEIGHT = 800, 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Triangular Peg Puzzle")

FONT = pygame.font.SysFont(None, 24)
TITLE_FONT = pygame.font.SysFont(None, 32)
STEP_FONT = pygame.font.SysFont(None, 20)

WHITE = (240, 240, 240)
BLACK = (20, 20, 20)
RED = (200, 60, 60)
GREEN = (60, 180, 60)
GRAY = (120, 120, 120)
YELLOW = (255, 200, 0)

RADIUS = 18

ROW_LENGTHS = [3, 4, 3, 2]
H_SPACING = 110
V_SPACING = H_SPACING * math.sqrt(3) / 2
DIRS = [(0, 1), (1, 0), (1, 1)]


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
INNER_TRIANGLE = {2, 6, 10, 9, 8, 5}

RING_A = [1, 2, 6, 9, 8, 4]
RING_B = [2, 3, 7, 10, 9, 5]
RING_C = [5, 6, 10, 12, 11, 8]

DEFAULT_COLORS = {
    1: RED,
    2: GREEN,
    3: RED,
    4: GREEN,
    5: RED,
    6: GREEN,
    7: RED,
    8: GREEN,
    9: RED,
    10: GREEN,
    11: RED,
    12: GREEN,
}

start_colors = DEFAULT_COLORS.copy()


def cycle_color(current):
    if current is None:
        return RED
    if current == RED:
        return GREEN
    return None


def color_name(value):
    if value == RED:
        return "RED"
    if value == GREEN:
        return "GREEN"
    return "None"


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


def anim_button_layout():
    btn_w = [110, 110, 120]
    btn_h = 40
    gap = 20
    total_w = sum(btn_w) + gap * 2
    start_x = (WIDTH - total_w) // 2
    y = HEIGHT - 60
    rects = [
        pygame.Rect(start_x, y, btn_w[0], btn_h),
        pygame.Rect(start_x + btn_w[0] + gap, y, btn_w[1], btn_h),
        pygame.Rect(start_x + btn_w[0] + gap + btn_w[1] + gap, y, btn_w[2], btn_h),
    ]
    return rects


def solve_full_bfs(seed_state):
    start_key = serialize(seed_state)
    if is_goal(seed_state):
        return []
    q = deque([(start_key, seed_state, [])])
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


def node_at_pos(pos):
    for i, (x, y) in NODES.items():
        dist = math.hypot(pos[0] - x, pos[1] - y)
        if dist <= RADIUS:
            return i
    return None


def draw_board(state, title_text, message="", highlight=None, instructions=None, step_panel=None, center_message=None, do_flip=True):
    SCREEN.fill(WHITE)
    title = TITLE_FONT.render(title_text, True, BLACK)
    SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))

    y = 60
    if center_message:
        mid = FONT.render(center_message, True, BLACK)
        SCREEN.blit(mid, (WIDTH // 2 - mid.get_width() // 2, y))
        y += 28

    if instructions:
        for line in instructions:
            txt = FONT.render(line, True, BLACK)
            SCREEN.blit(txt, (20, y))
            y += 22

    for a, b in EDGES:
        ax, ay = NODES[a]
        bx, by = NODES[b]
        pygame.draw.line(SCREEN, GRAY, (int(ax), int(ay)), (int(bx), int(by)), 3)

    highlight = set(highlight or [])
    for i, (x, y) in NODES.items():
        color = state.get(i)
        if i in highlight:
            pygame.draw.circle(SCREEN, YELLOW, (int(x), int(y)), RADIUS + 5, 3)
        if color is not None:
            pygame.draw.circle(SCREEN, color, (int(x), int(y)), RADIUS)
        else:
            pygame.draw.circle(SCREEN, GRAY, (int(x), int(y)), RADIUS, 2)
        label = FONT.render(str(i), True, BLACK)
        SCREEN.blit(label, (int(x) - 6, int(y) - 28))

    if message:
        msg = FONT.render(message, True, BLACK)
        SCREEN.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT - 110))

    if step_panel:
        panel_y = 430
        if step_panel.get("title"):
            header = STEP_FONT.render(step_panel["title"], True, BLACK)
            header_x = WIDTH // 2 - header.get_width() // 2
            SCREEN.blit(header, (header_x, panel_y))
            panel_y += 22
        max_w = 0
        rendered = []
        for i, text in enumerate(step_panel["lines"]):
            color = step_panel["colors"][i]
            surf = STEP_FONT.render(text, True, color)
            rendered.append(surf)
            max_w = max(max_w, surf.get_width())
        start_x = WIDTH // 2 - max_w // 2
        for surf in rendered:
            SCREEN.blit(surf, (start_x, panel_y))
            panel_y += 20

    if do_flip:
        pygame.display.flip()


def main():
    mode = "menu"  # menu, setup, interactive, animation
    peg_colors = start_colors.copy()
    anim_state = None
    message = ""
    clock = pygame.time.Clock()

    def reset_to_start():
        return start_colors.copy()

    def start_animation_state():
        seq = solve_full_bfs(start_colors)
        history = [start_colors.copy()]
        return {
            "seq": seq,
            "history": history,
            "idx": 0,
            "auto": False,
            "acc": 0.0,
        }

    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if mode == "menu":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos
                    if 80 <= x <= 280 and 150 <= y <= 200:
                        mode = "setup"
                        peg_colors = start_colors.copy()
                    elif 80 <= x <= 280 and 230 <= y <= 280:
                        mode = "animation"
                        anim_state = start_animation_state()
                    elif 80 <= x <= 280 and 310 <= y <= 360:
                        mode = "interactive"
                        peg_colors = start_colors.copy()

            elif mode == "setup":
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE, pygame.K_m):
                        start_colors.update(peg_colors)
                        mode = "menu"
                    elif event.key == pygame.K_r:
                        peg_colors = DEFAULT_COLORS.copy()
                        start_colors.update(peg_colors)
                    elif event.key == pygame.K_p:
                        out = {i: color_name(c) for i, c in peg_colors.items()}
                        print("Current mapping (dict):", out)
                        print("Current mapping (lines):")
                        for k in sorted(out):
                            print(f" {k}: {out[k]},")
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    node = node_at_pos(event.pos)
                    if node:
                        peg_colors[node] = cycle_color(peg_colors.get(node))
                        start_colors[node] = peg_colors[node]
                        message = f"Node {node} -> {color_name(peg_colors[node])}"

            elif mode == "interactive":
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE, pygame.K_m):
                        mode = "menu"
                    elif event.key == pygame.K_r:
                        peg_colors = reset_to_start()
                        message = "Reset to start"
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    node = node_at_pos(event.pos)
                    if node:
                        if node == 1:
                            peg_colors = rotate(peg_colors, RING_A, True)
                            message = "Ring A clockwise"
                        elif node == 4:
                            peg_colors = rotate(peg_colors, RING_A, False)
                            message = "Ring A counter-clockwise"
                        elif node == 3:
                            peg_colors = rotate(peg_colors, RING_B, False)
                            message = "Ring B counter-clockwise"
                        elif node == 7:
                            peg_colors = rotate(peg_colors, RING_B, True)
                            message = "Ring B clockwise"
                        elif node == 11:
                            peg_colors = rotate(peg_colors, RING_C, True)
                            message = "Ring C clockwise"
                        elif node == 12:
                            peg_colors = rotate(peg_colors, RING_C, False)
                            message = "Ring C counter-clockwise"
                        else:
                            message = "Use 1/4, 3/7, 11/12 to rotate"

            elif mode == "animation":
                if anim_state is None:
                    anim_state = start_animation_state()
                seq = anim_state["seq"]
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE, pygame.K_m):
                        mode = "menu"
                    elif event.key == pygame.K_r:
                        anim_state = start_animation_state()
                    elif event.key == pygame.K_SPACE:
                        if seq:
                            anim_state["auto"] = not anim_state["auto"]
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and seq:
                    rects = anim_button_layout()
                    if rects[0].collidepoint(event.pos):
                        if anim_state["idx"] > 0:
                            anim_state["history"].pop()
                            anim_state["idx"] -= 1
                    elif rects[1].collidepoint(event.pos):
                        if anim_state["idx"] < len(seq):
                            move = seq[anim_state["idx"]]
                            cycle, cw = MOVES[move]
                            new_state = rotate(anim_state["history"][anim_state["idx"]], cycle, cw)
                            anim_state["history"].append(new_state)
                            anim_state["idx"] += 1
                    elif rects[2].collidepoint(event.pos):
                        anim_state["auto"] = not anim_state["auto"]

        # Per-frame updates for animation auto-play
        if mode == "animation" and anim_state and anim_state["seq"]:
            if anim_state["auto"] and anim_state["idx"] < len(anim_state["seq"]):
                anim_state["acc"] += dt
                if anim_state["acc"] >= 1.2:
                    anim_state["acc"] = 0.0
                    move = anim_state["seq"][anim_state["idx"]]
                    cycle, cw = MOVES[move]
                    new_state = rotate(anim_state["history"][anim_state["idx"]], cycle, cw)
                    anim_state["history"].append(new_state)
                    anim_state["idx"] += 1
            if anim_state["auto"] and anim_state["idx"] >= len(anim_state["seq"]):
                anim_state["auto"] = False

        # Drawing per mode
        if mode == "menu":
            SCREEN.fill(WHITE)
            title = TITLE_FONT.render("Triangular Peg Puzzle", True, BLACK)
            SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, 40))
            items = ["1. Setup", "2. Solve & Animation", "3. Demo (Interactive)"]
            y = 140
            for text in items:
                rect = pygame.Rect(80, y, 200, 50)
                pygame.draw.rect(SCREEN, GRAY, rect, border_radius=6)
                label = FONT.render(text, True, BLACK)
                SCREEN.blit(label, (rect.x + (rect.width - label.get_width()) // 2, rect.y + 15))
                y += 80
            pygame.display.flip()

        elif mode == "setup":
            draw_board(
                peg_colors,
                "Setup (Configurator)",
                message=message,
                instructions=[
                    "Click a node to cycle empty -> red -> green",
                    "R: reset defaults    P: print mapping    M/Esc: menu",
                ],
            )

        elif mode == "interactive":
            draw_board(
                peg_colors,
                "Demo (Interactive)",
                message=message,
                instructions=[
                    "Click nodes: 1/4 (Ring A cw/ccw), 3/7 (Ring B ccw/cw), 11/12 (Ring C cw/ccw)",
                    "M/Esc: menu    R: reset to setup layout",
                ],
            )

        elif mode == "animation":
            seq = anim_state["seq"] if anim_state else None
            if not seq:
                draw_board(start_colors, "Solve & Animation", message="No solution found for this layout", instructions=["M/Esc: menu", "R: recompute from setup layout"], step_panel=None)
            else:
                idx = anim_state["idx"]
                current_state = anim_state["history"][idx]
                step_status = f"Step {idx}/{len(seq)}"
                if idx < len(seq):
                    step_status += f" | Next: {move_label(seq[idx])}"
                else:
                    step_status += " | Done"
                lines = []
                colors = []
                # Initial state marker
                if idx == 0:
                    init_prefix = "> "
                    init_color = GREEN
                else:
                    init_prefix = "  "
                    init_color = GRAY
                lines.append(init_prefix + "0. Start state")
                colors.append(init_color)
                for i, m in enumerate(seq):
                    prefix = "✓ " if (i + 1) < idx else "> " if (i + 1) == idx else "  "
                    lines.append(prefix + f"{i + 1}. {move_label(m)}")
                    if (i + 1) < idx:
                        colors.append(GRAY)
                    elif (i + 1) == idx:
                        colors.append(GREEN)
                    else:
                        colors.append(BLACK)
                draw_board(
                    current_state,
                    "Solve & Animation",
                    message="SPACE/Play toggles auto; Prev/Next step; R: restart; M/Esc: menu",
                    highlight=MOVES[seq[idx - 1]][0] if idx > 0 else None,
                    step_panel={"title": "Steps", "lines": lines, "colors": colors},
                    center_message=step_status,
                    do_flip=False,
                )
                # Buttons (centered)
                rects = anim_button_layout()
                y = rects[0].y
                labels = ["Prev", "Next", "Play" if not anim_state["auto"] else "Pause"]
                colors_btn = [GRAY, GRAY, GREEN if anim_state["auto"] else GRAY]
                for rect, label, bg in zip(rects, labels, colors_btn):
                    pygame.draw.rect(SCREEN, bg, rect, border_radius=6)
                    txt = FONT.render(label, True, BLACK)
                    SCREEN.blit(txt, (rect.x + (rect.width - txt.get_width()) // 2, rect.y + 10))
                pygame.display.flip()


if __name__ == "__main__":
    main()