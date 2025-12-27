
<img width="1222" height="325" alt="machinarium-gitjib nammmer" src="https://github.com/user-attachments/assets/4ead73c8-fb1b-4be4-a70e-6ee57f29c799" />

# Triangular Peg Puzzle

A single-file, menu-driven Pygame app for the triangular peg solitaire variant, with configurator, solver, and animated playback from the game [machinarium](https://store.epicgames.com/en-US/p/machinarium-5e6c71)


![Platform](https://img.shields.io/badge/platform-Windows-blue)
![Build](https://img.shields.io/badge/build-PyInstaller-green)

 ##  📦Downloads: 

[![Download for Windows](https://img.shields.io/badge/Download-Windows%20EXE-blue?style=for-the-badge&logo=windows)](https://github.com/xXWarMachineRoXx/tripeg-solitaire/releases/latest)


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




![Platform](https://img.shields.io/badge/platform-Windows-blue)
![Build](https://img.shields.io/badge/build-PyInstaller-green)

### Click this button to download

[![Download for Windows](https://img.shields.io/badge/Download-Windows%20EXE-blue?style=for-the-badge&logo=windows)](https://github.com/xXWarMachineRoXx/tripeg-solitaire/releases/latest)

No Python installation required.
