# Triangular Peg Puzzle

A single-file, menu-driven Pygame app for the triangular peg solitaire variant, with configurator, solver, and animated playback.

## Demo

[![Triangular Peg Puzzle – Solver & Animation Demo](https://img.youtube.com/vi/7BQTCahj8Q0/maxresdefault.jpg)](https://youtu.be/7BQTCahj8Q0)



## Features
- Unified menu:
  - **Setup (Configurator)**: click pegs to cycle empty → red → green; save start layout.
  - **Solve & Animation**: runs the solver for the inner-triangle goal, shows steps under the board, play/pause, prev/next, and highlights the active ring.
  - **Demo (Interactive)**: manual ring rotations on the live board.
- Correct board edges and rotation directions.
- HUD polish: centered status, step list (start state = step 0), non-flickering controls.

## Install
```bash
pip install -r requirements.txt
```

## Run
```bash
python main.py
```

## Controls

### Global
- **M / Esc**: back to menu
- **R**: reset the current mode to the configured start layout

### Setup
- **Click node**: cycle empty → red → green
- **R**: reset to defaults
- **P**: print mapping

### Demo (Interactive)
- **Click 1**: Ring A clockwise
- **Click 4**: Ring A counter-clockwise
- **Click 3**: Ring B counter-clockwise
- **Click 7**: Ring B clockwise
- **Click 11**: Ring C clockwise
- **Click 12**: Ring C counter-clockwise

### Solve & Animation
- **Prev / Next buttons**: step backward/forward
- **Play button or Space**: toggle auto-play
- **R**: restart animation from the configured layout
- **Highlight**: active ring nodes are outlined yellow each step
- Status shows `Step X/N | Next: <move>` and a steps list under the board (step 0 = start state).

## Goal
The solver aims to make the inner triangle `{2, 6, 10, 9, 8, 5}` all green.

## Notes
- Tested on Windows with Python + Pygame. 
- `requirements.txt` lists runtime dependencies.