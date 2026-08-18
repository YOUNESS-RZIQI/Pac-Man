# AGENTS.md

## Source of truth
- `Project_Subject.md` is the **authoritative spec** for this project. Read it fully before writing code and re-check it whenever requirements are ambiguous. Never invent requirements beyond it.

## Quality gates (peer-reviewed, non-negotiable)
- Python 3.10+, **flake8** standard, **mypy** static typing. Exact lint command (Makefile `lint`):
  `flake8 . && mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs`
  (`lint-strict` = same with `mypy . --strict`).
- Type hints on every parameter/return; PEP 257 docstrings (Google/NumPy style).
- **Never crash / never print a Python traceback.** Any bad input (missing file, invalid config) must yield a clean message. Use try-except + context managers; resource leaks fail review.
- `.gitignore` Python artifacts (`__pycache__`, `.mypy_cache`, `.venv`). Unit tests via pytest/unittest are expected but not submitted.

## Makefile contract (must exist)
- Rules: `install`, `run`, `debug` (pdb), `clean`, `lint`, `lint-strict` (see above).

## CLI + config
- Launch: `python3 pac-man.py config.json` — exactly one arg, a JSON file.
- Config is JSON but must accept `#` line comments; unknown keys ignored; missing/invalid values clamp to safe defaults with a clear log message. Document keys + defaults in README.

## Architecture constraints
- Modular OOP. GUI library must be MLX or similar: **every function used must have an MLX equivalent**, otherwise it's disallowed.
- **Maze generation: integrate the assigned external `A-Maze-ing` package as-is — never write your own generator.** Loader adapts to their interface (package is re-installed during peer review). Call with `PERFECT=False` for Pac-Man corridors; handle generator failure cleanly.

## Game spec gotchas
- ≥10 levels; level 1 uses fixed `seed: 42`, later levels random. Player spawns in the middle; 4 ghosts + 4 super-pacgums in the 4 corners; pacgums in most corridors; 3 lives, respawn in the middle.
- Cheat mode required for peer review: invincibility, level skip, ghost freeze, extra lives, speed.
- HUD always visible: score, lives, level, remaining time. Pause + resume. Main menu: Start / View Highscores / Instructions / Exit. Game-over and victory screens collect the player name for the highscore.

## Highscore system
- Top-10, persisted (e.g. json on disk), robust to file errors. Names ≤10 chars, alphanumeric + spaces only; scores non-negative integers. Load at start, save at game end, displayed in main menu.

## Mandated deliverables
- `README.md` at root: first line italicized 42-credits line, then Description, Instructions, Resources (+how AI was used), Configuration, Highscore, Maze Generation, Implementation, General Software Architecture, Project Management (linking the PM dir). English only.
- Packaging script/spec at repo root (deployable to Steam/Itch.io as free/unlisted).
- Project-management artifacts (timeline, progress tracking, risk analysis, team org, acceptance tests) in a dedicated subdirectory.
