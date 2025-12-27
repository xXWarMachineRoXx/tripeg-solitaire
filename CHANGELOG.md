# Changelog

## 🎉 v1.0.0 (LTS Release · Latest · Stable)
- Unified menu-driven main (Setup configurator, Solve & Animation, Demo).
- Solver targets inner-triangle goal; animation supports play/pause and prev/next with ring highlights.
- Step list under the board (start state = step 0); aligned controls and centered HUD with reduced flicker.
- Corrected board edges and rotation directions.

### Recap
- `main.py` hosts a single menu for Setup, Solve & Animation, and Demo (interactive rotation).
- Configurator sets start colors; solver runs path with animated playback and a step list.
- UI polish: centered HUD, non-flickering controls, and spaced help text.


## v0.4.0
- Unified app into a single menu-driven main: Setup (configurator), Solve & Animation, and Demo (interactive).
- Centered animation HUD: step/next banner, steps list under the board with start state as step 0, and aligned buttons with correct hitboxes.
- Reduced UI flicker, spaced controls/help text, and kept solver/animation in sync with configured start colors.

## v0.3.0
- Added configurator tool to interactively set peg colors (click to cycle empty/red/green, print mappings in dict and multi-line formats).
- Improved mapping readability in configurator (color names shown in UI messages).

## Release v0.2.0
Release v0.2.0 (Latest)
@maintainer released this today
· 0 commits to main since this release
Tag: v0.2.0
Commit: pending
📦 Downloads: source only (add link if hosting binaries)

### What's Changed
- Fixed board edges and ring directions to match the target layout.
- Solver targets the inner-triangle green goal; BFS finds the 5-move solution.
- Animation player gains play/pause, prev/next, highlighted ring steps, and a textual step list.

### Full Changelog
- v0.1.0...v0.2.0

## v0.2.0
- Fixed board edges and ring directions to match the target layout.
- Solver targets the inner-triangle green goal; BFS finds the 5-move solution.
- Animation player gains play/pause, prev/next, highlighted ring steps, and a textual step list.

## v0.1.0
- Initial playable board with colored pegs and basic solver + animation.
