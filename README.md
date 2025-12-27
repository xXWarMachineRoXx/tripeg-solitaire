# Peg Solitaire Machinirium

A single-screen pygame app that combines the configurator, solver, animation, and demo for the triangular peg puzzle with ring rotations.

## Features
- Menu-driven flow: Setup, Solve & Animation, and Demo (interactive ring control)
- BFS solver targeting the inner-triangle green goal
- Step list with start-state entry, next-step banner, Prev/Next/Play controls
- Configurable starting layout saved back to the solver/animation

## Install
1) Use Python 3.10+.
2) Install deps: `pip install -r requirements.txt`

## Run
`python main.py`

## Modes and Controls
### Setup (Configurator)
- Click a node to cycle empty → red → green
- Keys: `R` reset defaults, `P` print mapping to console, `M`/`Esc` back to menu

### Solve & Animation
- Space or Play toggles auto-play; Prev/Next step through the solution
- `R` recompute from the current setup layout; `M`/`Esc` back to menu
- Step list shows step 0 start state and highlights current step; next move appears under the title

### Demo (Interactive)
- Click nodes to rotate rings: 1/4 (Ring A cw/ccw), 3/7 (Ring B ccw/cw), 11/12 (Ring C cw/ccw)
- `R` reset to the configured start layout; `M`/`Esc` back to menu

## Notes
- Legacy standalone scripts live in `dev/` for reference; `main.py` is the authoritative entry point.
