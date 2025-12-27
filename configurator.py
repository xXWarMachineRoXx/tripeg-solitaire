import sys
import math
import pygame

pygame.init()

# Window
WIDTH, HEIGHT = 800, 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Peg Board Configurator")
FONT = pygame.font.SysFont(None, 24)
TITLE_FONT = pygame.font.SysFont(None, 32)

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

# Default layout (matches animation/main start state)
DEFAULT_COLORS = {
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
    11: RED,
    12: GREEN,
}

peg_colors = DEFAULT_COLORS.copy()


def color_name(value):
    if value == RED:
        return "RED"
    if value == GREEN:
        return "GREEN"
    return "None"


def mapping_as_lines(state: dict[int, tuple[int, int, int]]) -> str:
    lines = []
    for k in sorted(state):
        lines.append(f" {k}: {color_name(state[k])},")
    return "\n".join(lines)


def cycle_color(current):
    if current is None:
        return RED
    if current == RED:
        return GREEN
    return None


def node_at_pos(pos):
    for i, (x, y) in NODES.items():
        dist = math.hypot(pos[0] - x, pos[1] - y)
        if dist <= RADIUS:
            return i
    return None


def draw_board(message=""):
    SCREEN.fill(WHITE)
    title = TITLE_FONT.render("Configurator", True, BLACK)
    SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))

    instructions = [
        "Click a node to cycle: empty -> red -> green -> empty",
        "C: clear all    R: reset to default    P: print mapping",
        "ESC/Q: quit",
    ]
    y = 60
    for line in instructions:
        txt = FONT.render(line, True, BLACK)
        SCREEN.blit(txt, (20, y))
        y += 24

    for a, b in EDGES:
        ax, ay = NODES[a]
        bx, by = NODES[b]
        pygame.draw.line(SCREEN, GRAY, (int(ax), int(ay)), (int(bx), int(by)), 3)

    for i, (x, y) in NODES.items():
        color = peg_colors.get(i)
        if color is not None:
            pygame.draw.circle(SCREEN, color, (int(x), int(y)), RADIUS)
        else:
            pygame.draw.circle(SCREEN, GRAY, (int(x), int(y)), RADIUS, 2)
        label = FONT.render(str(i), True, BLACK)
        SCREEN.blit(label, (int(x) - 6, int(y) - 28))

    if message:
        msg = FONT.render(message, True, BLACK)
        SCREEN.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT - 40))

    pygame.display.flip()


def print_mapping():
    out = {i: color_name(c) for i, c in peg_colors.items()}
    print("Current mapping (dict):")
    print(out)
    print("Current mapping (lines):")
    print(mapping_as_lines(peg_colors))


def main():
    global peg_colors
    clock = pygame.time.Clock()
    message = ""
    running = True
    while running:
        _dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
                elif event.key == pygame.K_c:
                    peg_colors = {i: None for i in peg_colors}
                    message = "Cleared"
                elif event.key == pygame.K_r:
                    peg_colors = DEFAULT_COLORS.copy()
                    message = "Reset to default"
                elif event.key == pygame.K_p:
                    print_mapping()
                    message = "Mapping printed to console"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                node = node_at_pos(event.pos)
                if node is not None:
                    peg_colors[node] = cycle_color(peg_colors.get(node))
                    message = f"Node {node} -> {color_name(peg_colors[node])}"
        draw_board(message)
    pygame.quit()


if __name__ == "__main__":
    main()
