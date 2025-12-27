import pygame
import sys
import math

pygame.init()

WIDTH, HEIGHT = 800, 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Triangular Peg Solitaire")

FONT = pygame.font.SysFont(None, 24)
TITLE_FONT = pygame.font.SysFont(None, 32)

WHITE = (240, 240, 240)
BLACK = (20, 20, 20)
RED = (200, 60, 60)
GREEN = (60, 180, 60)
GRAY = (120, 120, 120)
YELLOW = (255, 200, 0)

RADIUS = 18

# Board requested: rows of 3, 4, 3, 2 (top to bottom) -> 12 nodes total.
ROW_LENGTHS = [3, 4, 3, 2]
H_SPACING = 110
V_SPACING = H_SPACING * math.sqrt(3) / 2


def build_layout():
    nodes = {}
    coords = {}  # (r, c) -> node id
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


DIRS = [(0, 1), (1, 0), (1, 1)]  # base lattice directions


def build_edges(coords):
    edges = set()
    for (r, c), a in coords.items():
        for dr, dc in DIRS:
            b = coords.get((r + dr, c + dc))
            if b:
                edges.add(tuple(sorted((a, b))))
    # Apply manual adjustments to match the desired graph
    remove_edges = {(4, 9), (5, 10), (8, 12)}
    add_edges = {(5, 8), (7, 10), (10, 12),(9, 11),(6, 9)}

    edges = {tuple(sorted(e)) for e in edges}
    edges -= {tuple(sorted(e)) for e in remove_edges}
    edges |= {tuple(sorted(e)) for e in add_edges}

    return sorted(edges)


def build_valid_jumps(coords):
    jumps = set()
    for (r, c), s in coords.items():
        for dr, dc in DIRS:
            j = coords.get((r + dr, c + dc))
            t = coords.get((r + 2 * dr, c + 2 * dc))
            if j and t:
                jumps.add((s, j, t))
    return jumps


NODES, COORDS = build_layout()
EDGES = build_edges(COORDS)
VALID_JUMPS = build_valid_jumps(COORDS)
INNER_TRIANGLE = {2, 6, 10, 9, 8, 5}

# Precompute rows for text logging (node order matches visual rows)
ROW_NODES = []
idx = 1
for length in ROW_LENGTHS:
    ROW_NODES.append([idx + i for i in range(length)])
    idx += length

# -------------------------------------------------
# Initial state (peg colors per node; None would mean empty)
# Color layout approximates the reference puzzle.
# -------------------------------------------------
label_map = {i: i for i in NODES}
peg_colors = {
    # Row 0 (3 nodes)
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
# START_COLORS = {
#      1: RED,
#     2: GREEN,
#     3: RED,
#     4: GREEN,
#     5: RED,
#     6: GREEN,
#     7: GREEN,
#     8: RED,
#     9: GREEN,
#     10: RED,
#     11: RED,
#     12: GREEN,
# }
state = {i: True for i in NODES}  # kept for compatibility, not used for moves


def color_char(node_id):
    color = peg_colors.get(node_id)
    if color == RED:
        return "R"
    if color == GREEN:
        return "G"
    return "."


def format_state_lines():
    lines = []
    for row in ROW_NODES:
        parts = []
        for node in row:
            label = label_map.get(node, node)
            parts.append(f"{node}:{label}:{color_char(node)}")
        lines.append(" ".join(parts))
    return lines


def log_state(prefix=""):
    lines = format_state_lines()
    header = f"[STATE] {prefix}" if prefix else "[STATE]"
    print(header)
    for ln in lines:
        print("  " + ln)

def is_valid_jump(source, jumped, target):
    """Validate a jump move"""
    if not state.get(source, False):
        return False, "Source must have a peg"
    if not state.get(jumped, False):
        return False, "Jumped position must have a peg"
    if state.get(target, True):
        return False, "Target must be empty"
    
    if (source, jumped, target) not in VALID_JUMPS:
        return False, "Move must follow board lines"

    return True, "Valid move"

def apply_action(source, jumped, target):
    """Execute a valid jump"""
    state[source] = False
    state[jumped] = False
    state[target] = True

def count_pegs():
    """Count remaining pegs"""
    return sum(1 for v in peg_colors.values() if v is not None)

def check_win():
    """Win when all inner-triangle nodes are green."""
    return all(peg_colors.get(node) == GREEN for node in INNER_TRIANGLE)

# -------------------------------------------------
# UI helpers
# -------------------------------------------------
def draw_board(selected, message=""):
    SCREEN.fill(WHITE)
    
    # Draw title
    title = TITLE_FONT.render("Triangular Peg Solitaire", True, BLACK)
    SCREEN.blit(title, (WIDTH//2 - title.get_width()//2, 20))
    
    # Draw instructions
    instructions = [
        "Click 1: rotate ring clockwise",
        "Click 4: rotate ring counter-clockwise",
        "Ring A: 1-2-6-9-8-4 around center 5",
        "Click 3: rotate ring counter-clockwise (center 6)",
        "Click 7: rotate ring clockwise (center 6)",
        "Ring B: 2-3-7-10-9-5 around center 6",
        "Click 11: rotate ring clockwise (center 9)",
        "Click 12: rotate ring counter-clockwise (center 9)",
        "Ring C: 5-6-10-12-11-8 around center 9",
        "Press R to reset",
        f"Pegs remaining: {count_pegs()}"
    ]
    
    y_offset = 60
    for inst in instructions:
        text = FONT.render(inst, True, BLACK)
        SCREEN.blit(text, (20, y_offset))
        y_offset += 25

    # Draw board edges to mirror the reference shape
    for a, b in EDGES:
        ax, ay = NODES[a]
        bx, by = NODES[b]
        pygame.draw.line(SCREEN, GRAY, (int(ax), int(ay)), (int(bx), int(by)), 3)
    
    # Draw message
    if message:
        msg_color = GREEN if "Valid" in message or "Win" in message else RED
        msg_text = FONT.render(message, True, msg_color)
        SCREEN.blit(msg_text, (WIDTH//2 - msg_text.get_width()//2, HEIGHT - 50))
    
    # Draw nodes
    for i, (x, y) in NODES.items():
        # Draw peg or empty hole
        color = peg_colors.get(i)
        if color is not None:
            pygame.draw.circle(SCREEN, color, (int(x), int(y)), RADIUS)
        else:
            pygame.draw.circle(SCREEN, GRAY, (int(x), int(y)), RADIUS, 2)
        
        # Highlight last clicked node
        if i in selected:
            pygame.draw.circle(SCREEN, YELLOW, (int(x), int(y)), RADIUS + 5, 3)
        
        # Draw node number
        label_value = label_map.get(i, i)
        label = FONT.render(str(label_value), True, BLACK)
        SCREEN.blit(label, (int(x) - 6, int(y) - 35))
    
    # Optional win banner, but never show game over
    if check_win():
        win_text = TITLE_FONT.render("YOU WIN!", True, GREEN)
        SCREEN.blit(win_text, (WIDTH//2 - win_text.get_width()//2, HEIGHT//2))
    
    pygame.display.flip()

def node_at_pos(pos):
    """Find which node was clicked"""
    for i, (x, y) in NODES.items():
        dist = math.sqrt((pos[0] - x)**2 + (pos[1] - y)**2)
        if dist <= RADIUS:
            return i
    return None

# -------------------------------------------------
# Rotation mechanic
# -------------------------------------------------
RING_A = [1, 2, 6, 9, 8, 4]        # center 5
RING_B = [2, 3, 7, 10, 9, 5]       # center 6
RING_C = [5, 6, 10, 12, 11, 8]     # center 9


def rotate_ring(cycle, clockwise=True, name=""):
    peg_values = [peg_colors.get(i) for i in cycle]
    label_values = [label_map[i] for i in cycle]
    if clockwise:
        peg_values = peg_values[-1:] + peg_values[:-1]
        label_values = label_values[-1:] + label_values[:-1]
    else:
        peg_values = peg_values[1:] + peg_values[:1]
        label_values = label_values[1:] + label_values[:1]
    for i, v, lbl in zip(cycle, peg_values, label_values):
        label_map[i] = lbl
        peg_colors[i] = v
    log_state(f"{name} {'CW' if clockwise else 'CCW'}")


# -------------------------------------------------
# Main loop
# -------------------------------------------------
selected = []
message = ""
message_timer = 0

clock = pygame.time.Clock()

while True:
    dt = clock.tick(60)
    
    # Fade message
    if message_timer > 0:
        message_timer -= dt
        if message_timer <= 0:
            message = ""
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:  # Reset game
                label_map = {i: i for i in NODES}
                peg_colors = {
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
                state = {i: True for i in NODES}
                selected = []
                message = "Game reset"
                message_timer = 2000
                log_state("Reset")
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            node = node_at_pos(event.pos)
            if node is not None:
                selected = [node]
                if node == 1:
                    rotate_ring(RING_A, clockwise=True, name="Ring A")
                    message = "Ring A rotated clockwise"
                elif node == 4:
                    rotate_ring(RING_A, clockwise=False, name="Ring A")
                    message = "Ring A rotated counter-clockwise"
                elif node == 3:
                    rotate_ring(RING_B, clockwise=False, name="Ring B")
                    message = "Ring B rotated counter-clockwise"
                elif node == 7:
                    rotate_ring(RING_B, clockwise=True, name="Ring B")
                    message = "Ring B rotated clockwise"
                elif node == 11:
                    rotate_ring(RING_C, clockwise=True, name="Ring C")
                    message = "Ring C rotated clockwise"
                elif node == 12:
                    rotate_ring(RING_C, clockwise=False, name="Ring C")
                    message = "Ring C rotated counter-clockwise"
                else:
                    message = "Use 1/4, 3/7, 11/12 to rotate"
                message_timer = 1500
    
    draw_board(selected, message)