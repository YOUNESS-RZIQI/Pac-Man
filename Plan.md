Excellent question — this is exactly the right way to approach the project. Let me first extract what the subject *actually demands* from a GUI library, because that determines what you need to learn (and what you must *not* waste time on).

## Step 0 — Read the subject like an engineer, not a player

Here is what `Project_Subject.md` + your `AGENTS.md` force you to do with graphics, mapped to Pygame-ce skills:

| Subject requirement | Pygame-ce skill needed |
|---|---|
| III.2 Makefile `install/run/debug/clean/lint` | Setting up the env; `pdb` for debugging |
| IV "MLX or similar… each function you use has an equivalent in MLX" | **The guardrail that shapes this whole roadmap** (below) |
| V.1 CLI: `python3 pac-man.py config.json` | `sys.argv` (stdlib, not pygame) |
| V.2–V.3 JSON config with `#` comments, clamping | `json` + string handling (stdlib) |
| V.4 A-Maze-ing package integration (`PERFECT=False`) | Grid data structures → maze rendering |
| V.5 Highscore: top-10, name ≤10 alnum+spaces | Text input, JSON persistence |
| VI.1 Maze: walls/corridors, pacgums in corridors, 4 super-pacgums in 4 corners, 4 ghosts in corners, player in middle | Grid rendering, tile math |
| VI.2 Arrows/WASD, 3 lives, respawn in middle | Keyboard input, state reset |
| VI.3 Ghosts chase / flee / respawn after 5–10 s | Timers, simple AI, entity classes |
| VI.4 Pacgum +10, super +50, ghosts edible short time | Collision, timed states |
| VI.5 Cheat mode (invincible, skip, freeze, lives, speed) | Key toggles, game-state flags |
| VI.6 Scoring | Game state variables |
| VI.7 ≥10 levels, 90 s timer, pause/resume, keep score/lives | **State machine**, timers, level loop |
| VI.8 HUD always visible, Main/Pause/Game-over/Victory screens | Text rendering, menus, states |
| VII–VIII Packaging + PM docs | Not pygame at all |

### The MLX-equivalence guardrail (read this before everything)

`AGENTS.md` and subject IV require: **every pygame function you use must have an MLX equivalent**. MLX has: init, window, image buffer, put-image-to-window, pixel_put, string_put, key/mouse hooks, loop, destroy, color. That means:

- ✅ **Allowed / MLX-safe subset**: `pygame.init`, `display.set_mode/set_caption/flip`, `Surface`, `fill`, `draw.*`, `set_at`, `blit`, `event.get`, `key.get_pressed`, `KEYDOWN/KEYUP`, mouse events, `font.Font.render`, `time.monotonic()`, plain color tuples.
- ⚠️ **Gray zone you can justify**: `pygame.Rect` (a plain data structure, like a struct), `pygame.draw.circle` (equivalent to pixel-put loops), `pygame.time.Clock` (I recommend `time.monotonic()` instead — it's stdlib, zero debate).
- ❌ **Not allowed (no MLX equivalent)**: `pygame.mixer` (MLX has no audio), `pygame.sprite.Group` (MLX has no sprite system), `pygame.transform` (no scaling in MLX).

This is why the roadmap below teaches **concepts** (delta time, entities, collisions) but for the actual submission you'll implement them with MLX-equivalent primitives and your own OOP classes. Now, the roadmap.

---

# Pygame-ce Learning Roadmap for Pac-Man

## Stage 1 — Window, init/quit, display surface

**Concepts**
- A pygame program is: *init → create window → loop → quit*.
- `pygame.init()` starts every subsystem; `pygame.quit()` cleans up.
- `pygame.display.set_mode((w, h))` returns a **Surface** — the screen is just a pixel canvas you draw on.
- **Double buffering**: you draw on the back buffer, then `display.flip()` shows it. No flip = nothing appears.
- Structure matters from day 1: put everything in a `main()` and guard it with `if __name__ == "__main__":` — the Makefile `run` rule and `pdb` (`debug` rule) rely on a clean entry point.

**APIs**
| API | What it does |
|---|---|
| `pygame.init()` | Initializes all pygame modules |
| `pygame.display.set_mode((w, h))` | Creates the window, returns the screen Surface |
| `pygame.display.set_caption("Pac-Man")` | Window title |
| `pygame.display.flip()` | Shows what you drew |
| `pygame.quit()` | Releases everything |

**Exercises**
1. Open an 800×600 window titled "Pac-Man", fill it black, close it with the X button. Print `"bye"` on exit.
2. Keep it open for exactly 3 seconds using `time.sleep`, then quit — learn what "blocking the loop" does.
3. Fill the screen yellow, then `flip()`. Now remove the `flip()` and observe. Now draw nothing but keep `flip()` — observe.

**Mini-project**: none yet — window only.

**Explain before moving on**
- What is a Surface? What is the difference between the window and the surface?
- What does `flip()` do and what happens without it?
- Why must `pygame.quit()` run, and when does it *not* matter (OS kills the process anyway)?

**Common mistakes**
- Forgetting `flip()` → black window, panic.
- Calling `pygame.init()` inside the loop (it's once).
- `while True` without a quit path → frozen window.
- Using `time.sleep` in the loop → unresponsive window.

**Pac-Man connection**: V.1 (`python3 pac-man.py config.json`) and VI.8 (the game needs *one* window hosting menu, game, and end screens — the window itself never changes, only what's drawn on it).

---

## Stage 2 — The game loop and events

**Concepts**
- The game loop is `while running: handle events → update state → draw → flip`. This exact shape is your whole game.
- **Events** are messages pygame queues: window close, key press, mouse move, etc. You *poll* them every frame with `pygame.event.get()`.
- **Event vs state**: a key press is an event (happens once); holding a key is a state (true every frame). Pac-Man needs both: single presses for menu navigation, held keys for movement.
- This loop is the pygame equivalent of `mlx_loop` + `mlx_key_hook` — be able to say that out loud during peer review.

**APIs**
| API | What it does |
|---|---|
| `pygame.event.get()` | Returns a list of pending events for this frame |
| `event.type`, `event.key`, `event.mod` | Inspect an event |
| `pygame.QUIT`, `pygame.KEYDOWN`, `pygame.KEYUP` | Event type constants |
| `pygame.key.get_pressed()` | Returns all currently-held keys (a "state") |
| `pygame.K_LEFT`, `K_RIGHT`, `K_UP`, `K_DOWN`, `K_w`, `K_a`, `K_s`, `K_d`, `K_ESCAPE`, `K_RETURN`, `K_SPACE`, `K_p` | Key constants |

**Exercises**
1. Window that closes on `K_ESCAPE` (event-driven quit).
2. Print every key you press, using `event.key` and `pygame.key.name(event.key)`. Note how *one* press produces one event.
3. Hold a key: print a single line when it's *first* pressed, then a counter every frame while held (use `key.get_pressed()`).
4. Count `QUIT`-free frames and print FPS-ish count every second (`time.monotonic()`).

**Mini-project**: "Key inspector" — a window showing: last pressed key name, currently held keys, total event count. This teaches you the input model you'll rely on for the whole game.

**Explain before moving on**
- What's the difference between an *event* and a *state*? Give one example of each in Pac-Man.
- Why do we poll events every frame instead of "waiting" for a key?
- Which input model do you need for Pac-Man's 4-direction movement?

**Common mistakes**
- Checking `key.get_pressed()` inside a `KEYDOWN` branch (it's almost always true there — meaningless).
- `while not pygame.key.get_pressed()[...]` — blocks the event queue → frozen window.
- Mixing `event.key` (key constant) with `event.unicode` (character) — we'll need `unicode` later for the name entry.
- Forgetting `running = False` inside the QUIT handler.

**Pac-Man connection**: VI.2 (arrows/WASD movement), VI.5 (cheat keys), VI.8 (menu navigation with Enter/Esc/P).

---

## Stage 3 — Coordinates, colors, drawing primitives

**Concepts**
- Coordinate system: origin **(0,0) top-left**, x grows right, y grows **down**. This is the #1 mental model of pygame. The maze grid will map onto it.
- Colors are RGB tuples `(r, g, b)` 0–255 — the pygame equivalent of `mlx_create_trgb`.
- Drawing primitives draw **onto a Surface** — which can be the screen or an off-screen buffer. You always pass the target surface first: `pygame.draw.rect(screen, color, ...)`.
- **Paint order = draw order**: later draws cover earlier ones. This is how you layer maze → pellets → ghosts → player.

**APIs**
| API | What it does |
|---|---|
| `pygame.draw.rect(surface, color, rect)` | Filled rectangle |
| `pygame.draw.circle(surface, color, center, radius)` | Filled circle — pacgums, super-pacgums, Pac-Man |
| `pygame.draw.line(surface, color, start, end, width)` | Line — maze decoration if wanted |
| `pygame.draw.polygon(surface, color, points)` | Filled polygon — ghosts' bodies |
| `surface.fill(color)` | Paint whole surface one color |
| `surface.set_at((x, y), color)` | One pixel — the exact `mlx_pixel_put` twin |
| `surface.get_width()`, `get_height()`, `get_size()` | Window dimensions for centering |

**Exercises**
1. Black window, yellow circle in the center, radius 10 — "hello Pac-Man".
2. Draw 4 bigger yellow circles in the 4 corners (super-pacgums, VI.1) and a grid of small white circles (pacgums).
3. Draw a wall border of rectangles around the window edge.
4. Use `set_at` to draw a diagonal line pixel by pixel — understand how slow this is vs `draw.line` (performance intuition).

**Mini-project**: "Static maze mock" — a fixed 15×15 pattern of wall rects + corridor dots rendered from a hand-written 2D list. This is literally the rendering half of VI.1.

**Explain before moving on**
- Where is (0,0)? Where does y go? Why does this matter for the maze?
- What's the difference between drawing to the screen and drawing to an off-screen Surface?
- If pacgums must appear *under* the player but *above* walls, what order do you draw them in?

**Common mistakes**
- Not calling `flip()` after drawing → "where is my shape".
- Not `fill`-ing the screen each frame → trails/ghosting of previous frames.
- Confusing `pygame.draw.rect(screen, color, (x, y, w, h))` tuple form with `(left, top, width, height)` — remember it's *not* `(x, y, x2, y2)`.
- Treating the maze like a math plot (y up).

**Pac-Man connection**: VI.1 (walls/corridors/pacgums/super-pacgums) — the entire maze is primitives, no image assets needed.

---

## Stage 4 — Rectangles, movement, time-based movement

**Concepts**
- `pygame.Rect` stores `x, y, w, h` and gives named positions (`center`, `topleft`, `midleft`, `bottomright`…). It's a *data structure* (like a C struct) — safe under the MLX rule, and it's the basis of collisions in Stage 5.
- **Movement = changing position each frame.**
- **Frame-based vs time-based**: if you move 5 px per frame, the game speed changes with FPS. If you move `speed * dt` px per second, the game is identical at 30 or 144 FPS. Pac-Man must be time-based.
- `dt` = seconds since last frame. Compute it with `time.monotonic()` (stdlib — zero MLX debate; `pygame.time.Clock` is fine for a dev FPS cap, but keep the *game logic* on monotonic).
- Guard against huge `dt` (e.g., after a pause or a slow frame) — clamp it to avoid teleporting through walls.

**APIs**
| API | What it does |
|---|---|
| `pygame.Rect(x, y, w, h)` | Position + size container |
| `rect.x`, `rect.y`, `rect.center`, `rect.centerx`, `rect.centery`, `rect.topleft`, `rect.midright`… | Position accessors |
| `rect.move(dx, dy)`, `rect.move_ip(dx, dy)` | New rect / in-place move |
| `rect.clamp(target_rect)` | Keep rect inside another (bounds) |
| `time.monotonic()` | Stable clock, seconds, for `dt` |
| `pygame.time.Clock().tick(fps)` + `.get_fps()` | (Optional, dev-only) cap FPS and read it |

**Exercises**
1. A square that moves right at 5 px/frame — note speed varies with FPS.
2. Same square, but `x += 200 * dt` px/second. Cap the loop to 30 FPS and 60 FPS, verify speed is identical.
3. Keep the square inside the window: stop at edges (manual bounds + `clamp`).
4. Move in 4 directions with arrows using `key.get_pressed()` — held-key movement, this is VI.2's core.
5. Diagonal normalization: why moving left+up at 200 px/s makes you faster (Pythagoras)? Fix it by normalizing the direction vector.

**Mini-project**: "Bouncing ball" — time-based ball, bounces off 4 walls, speed constant regardless of FPS, and an on-screen FPS readout to prove it.

**Explain before moving on**
- Why is per-frame movement wrong? What does "pixels per second" mean and how do you compute it?
- What is `dt` and how do you compute it without `pygame.time.Clock`?
- Why must you clamp `dt`?

**Common mistakes**
- `speed = 5` px/frame → game speed changes on different machines.
- Integer-only positions: `x += speed * dt` where `speed*dt` < 1 truncates to 0 → square never moves at low FPS. Store positions as **floats**, assign to Rect only for drawing/collision.
- Forgetting to clamp `dt` after pause → player teleports through the map on resume.
- Holding keys but not using `key.get_pressed()` → stop-and-go movement.

**Pac-Man connection**: VI.2 (player speed, 4-direction movement), VI.3 (ghost speed), VI.5 (the "increased speed" cheat is literally `speed * multiplier`).

---

## Stage 5 — Collision detection

**Concepts**
- A collision is an overlap test. `Rect` makes it trivial for rectangles; for circles (Pac-Man, ghosts, pellets) use the **distance formula**: `dx² + dy² ≤ (r1 + r2)²`.
- Two styles you'll need:
  - **Free-movement collision** (Stage 5): move, then check overlap, then react.
  - **Grid collision** (Stage 8): ask "is the cell I'm moving into a wall?" — no rect lists needed.
- **Order matters**: move → check → resolve. If you check before moving, you get tunneling (object passes through at high speed).
- Collision is a *game-logic* concern: it changes score, lives, ghost state — not drawing. Keep it in `update()`, not in drawing code.

**APIs**
| API | What it does |
|---|---|
| `rect.colliderect(other)` | Rect-rect overlap test |
| `rect.collidepoint((x, y))` | Does a point fall inside? |
| `rect.collidelist(rect_list)` | First index hit (or -1) |
| `math.hypot(dx, dy)` | Distance — circle collisions |

**Exercises**
1. Two squares; print "HIT" when they overlap (use `colliderect`).
2. A + B: move A with arrows, B is static; B turns red while overlapping — the classic "danger zone" prototype (ghost contact).
3. A square pushed against a wall rect: implement pushback (slide along the wall) — move x, check, revert; move y, check, revert.
4. A circle collecting static dots: distance-based pickup with a counter (this is the Pacgum mechanic).

**Mini-project**: "Collect the dots" — one yellow circle you steer, 20 static dots, dots disappear on contact, score counter on screen, all dots collected → window prints "LEVEL CLEAR". This is Pac-Man stripped to its absolute core (VI.2 + VI.4 + VI.6).

**Explain before moving on**
- Why check collision *after* moving? What is tunneling?
- Rect collision vs circle collision: when would you use each in Pac-Man?
- Pac-Man vs pellet: is that a rect test or a distance test? Pac-Man vs ghost: same or different? Why?

**Common mistakes**
- Collision check before the move → misses overlaps.
- Comparing `rect.center` to a pellet's pixel position exactly → "I collected it only when perfectly centered". Use a radius/tolerance.
- Per-pixel or `pygame.mask` collision — massive overkill here (and `pygame.mask` has no MLX equivalent; avoid it).
- Jitter: object ends up *inside* a wall; fix by reverting the axis move instead of pushing back.

**Pac-Man connection**: VI.2 (lose life on ghost contact), VI.4 (pacgum/super-pacgum pickup), VI.6 (scoring triggers), VI.3 (edible-ghost eating).

---

## Stage 6 — Text, fonts, HUD, name entry

**Concepts**
- Text in pygame: `font.render(text, antialias, color)` returns a **Surface**, then you `blit` it. This maps to `mlx_string_put`.
- **Blitting** = copying one surface onto another at a position: `screen.blit(surface, (x, y))`. This is also how off-screen buffers (the pre-rendered maze, Stage 8) get shown.
- **HUD** (VI.8) is just text drawn *after* the game world every frame, always visible: score, lives, level, remaining time.
- **Text input** for the highscore name (V.5): listen to `KEYDOWN`, use `event.unicode` for the character, enforce ≤10 chars, alphanumeric + spaces only, Backspace deletes, Enter validates.
- Performance: `render()` is expensive — re-render only when the string changes, not every frame.

**APIs**
| API | What it does |
|---|---|
| `pygame.font.Font(None, size)` | Default font at a size (no asset needed) |
| `pygame.font.Font("path.ttf", size)` | Custom font file (optional, nice for the arcade look) |
| `font.render(text, True, color)` | Text → Surface |
| `font.size(text)` | Measure text for centering |
| `screen.blit(surf, (x, y))` | Copy surf onto screen |
| `event.unicode` | The character typed (for name entry) |
| `pygame.K_BACKSPACE`, `pygame.K_RETURN` | Editing keys |

**Exercises**
1. Center "SCORE: 0" in a window. Use `font.size()` to center it properly.
2. Score that increases every time you press a key — re-render only when it changes (print the render count to prove it).
3. A name-entry field: type, Backspace, limit to 10 chars, only letters/digits/spaces, Enter prints the result. (This *is* the V.5 mechanic.)
4. Build the full HUD: 4 lines — Score, Lives, Level, Time — laid out exactly like VI.8 demands.

**Mini-project**: "Coin counter" — reuse the Stage 5 collector: moving circle + coins + live HUD (score, time left via countdown, lives reset on contact) + victory text when done.

**Explain before moving on**
- Why is `render` called sparingly?
- What does `blit` actually do? How is drawing text different from drawing a circle?
- How do you enforce "max 10 chars, alphanumeric + spaces only" (V.5) at the input level?

**Common mistakes**
- Re-rendering text every frame → FPS drops; render into a variable, re-render on change.
- Rendering but forgetting to blit → "text exists but invisible".
- Using `event.key` for the character instead of `event.unicode` (keys don't tell you shift/case).
- Not clearing the input surface → typed characters stack on top of each other.

**Pac-Man connection**: V.5 (name entry, top-10 display in main menu), VI.8 (HUD always visible + all screens).

---

## Stage 7 — Game states: menu, pause, game-over, victory

**Concepts**
- The subject's game loop (Chapter IV + VI.8) is a **state machine**: `Main Menu → Game → (Pause ⇄ Game) → Game Over / Victory → Name entry → Main Menu`.
- A state controls three things: *what input means*, *what updates*, *what draws*. Menu keys ≠ game keys.
- Simplest robust model: a `state` string/enum + `if/elif` dispatch in the loop, or one `State` class per screen. For this project, a tiny hand-rolled state machine (no framework) is ideal and reviewable.
- **Transitions must reset state**: entering "game" resets score/lives/level; entering "game over" freezes the game world.
- Pause = a state that stops updating the world but still draws it (and still handles input).

**APIs**: none new — pure structure. Reuse: events, `key.get_pressed()`, drawing, fonts.

**Exercises**
1. Two states: "MENU" (press Enter → GAME), "GAME" (press Esc → MENU). Note that Esc in menu ≠ Esc in game.
2. Add PAUSE: `P` toggles it; while paused, world does not update, "PAUSED" is drawn on top (this is exactly VI.8's pause menu).
3. Add GAME_OVER and VICTORY states with the full name-entry flow from Stage 6.
4. Track elapsed time across states — prove that pause stops the clock (VI.7's 90 s level timer must not run while paused).

**Mini-project**: **"Arcade skeleton"** — the complete loop of the whole game, with placeholder content: Main Menu (Start / Instructions / Exit) → Game (collect 5 dots, 30 s timer, 3 lives) → Victory or Game Over → name entry → back to menu, with highscore list shown in the menu. No maze, no ghosts yet — just the *skeleton* that every screen in VI.8 plugs into.

**Explain before moving on**
- Draw the state diagram of the whole Pac-Man game (from Chapter IV's game loop). Label every transition and what triggers it.
- Why must the world stop updating when paused, and why must the menu still read keys?
- What state-specific data must be reset when "Start Game" is pressed?

**Common mistakes**
- Updating the world in every state (menu "plays" the game in the background).
- Input leaking: the pause key also triggers in the menu.
- Not resetting on transition → new game starts with the old score.
- Game-over logic buried inside the game state instead of a separate state.
- Pause counting down the level timer.

**Pac-Man connection**: VI.8 (all screens), VI.7 (pause/resume, time limit), Chapter IV game loop — this stage is the *architecture* of your entire game.

---

## Stage 8 — Grid, tile-based maze, grid movement (the Pac-Man core)

**Concepts**
- The A-Maze-ing package (V.4) will give you a **grid** of 0/1 (corridor/wall) with `PERFECT=False`. Your job is to *render* it and *play* on it.
- Represent the level as a **2D list**: `grid[y][x]` → cell type. Add your own codes: wall, corridor, pacgum, super-pacgum, ghost-start, player-start.
- **Grid coords ↔ pixel coords**: `pixel = cell * cell_size`; and for Pac-Man, movement *snaps to cells*: you move along corridors cell-by-cell, can only turn at cell centers, and "collision with wall" = "is the next cell a wall?".
- **Pre-render the static maze** (walls + pellets) once onto an off-screen Surface, then blit it each frame. This maps perfectly to the MLX model (`mlx_new_image` + `mlx_put_image_to_window`) and is a big performance win (don't draw 1000 rects per frame).
- Super-pacgums go exactly in the 4 maze corners; pacgums in "most corridors"; player starts center; 4 ghosts in 4 corners (VI.1).

**APIs**: `pygame.Surface((w, h))` (off-screen buffer), `surface.blit(...)`, `pygame.Rect` per cell, `math` — mostly data-structure and loop logic.

**Exercises**
1. Render a hardcoded 15×15 grid: wall cells black rects, corridor cells empty.
2. Parse an ASCII map (`#####`, `#...#`, `#.#.#`…) into a grid and render it — exactly how you'll consume A-Maze-ing output (V.4).
3. Place pacgums in corridors and 4 super-pacgums in the 4 corners; draw them small/big circles (VI.4, VI.1).
4. **Grid-locked movement**: a circle that moves cell-by-cell, stops at walls, only turns at cell centers. Input: held direction + last valid direction (Pac-Man queues the turn).
5. Pre-render the whole maze to one off-screen Surface; each frame just one blit. Measure FPS before/after.

**Mini-project**: "Pac-grid prototype" — grid maze + grid-locked player + pacgums in corridors + collection counter + "all eaten → next seed". You now have VI.1 + VI.2 + VI.4 without any ghosts.

**Explain before moving on**
- What's the difference between grid coordinates and pixel coordinates? Give the conversion formulas.
- How do you prevent a grid-locked player from crossing a wall?
- Why is pre-rendering the maze to a Surface good for both *performance* and *MLX compliance*?

**Common mistakes**
- Indexing `grid[y][x]` with pixel values → IndexError; always convert to cell coords first.
- Free-form diagonal movement cutting corners through walls (Pac-Man moves on the grid).
- Off-by-one: cell size 40 → maze of 15 cells needs 600 px, not 640.
- Float grid indices — round/snap before indexing.
- Re-drawing the maze from scratch every frame.

**Pac-Man connection**: V.4 (A-Maze-ing `PERFECT=False` integration), VI.1 (whole level structure), VI.2 (movement).

---

## Stage 9 — Multiple entities, ghost AI, timers, edible states, respawn

**Concepts**
- **OOP entities**: `Player`, `Ghost`, `Pellet` classes, each with `update(dt, ...)` and `draw(screen)`. This satisfies AGENTS.md's "modular OOP" and avoids `pygame.sprite` (which has no MLX equivalent).
- Manage them in **lists** (`ghosts: list[Ghost]`, `pellets: list[Pellet]`) — iterate to update/draw/remove.
- **Timers** are *not* `time.sleep` — they're stored deadlines: `edible_until = time.monotonic() + 8.0`. Sleep freezes everything; deadlines don't. This is VI.3's "respawn after 5 or 10 s" and VI.7's 90 s level timer.
- **Ghost AI** (VI.3): chase = move toward the player, flee = move away, using BFS on the grid for shortest path (a perfect, small exercise; the maze is small, BFS per frame is fine). Each ghost can differ (Blinky chases, Pinky ambushes… — your own choice, "distance-based, random, etc." is explicitly allowed).
- **Edible state** (VI.4): eating a super-pacgum flips all ghosts to edible for a short time — one shared deadline; blink in the last ~2 s as a warning.
- **Respawn** (VI.2/VI.3): player death → reposition to center; eaten ghost → back to its corner after the timer.

**APIs**: `time.monotonic()`, `collections.deque` for BFS, `math` — plus everything from Stages 1–8. Nearly zero new pygame.

**Exercises**
1. Three colored squares with three behaviors: one follows (moves toward you), one flees (moves away), one patrols. Watch them interact.
2. On your Pac-grid from Stage 8: implement BFS shortest path; a "ghost" circle follows the path to your position. Print the path length.
3. Timer practice: a square that changes color every 2 s using deadlines (not sleep). Then: blinks during the last second.
4. Death + respawn: player touches ghost → reset to center, 1 life lost; ghost eaten → removed, returns to corner after 5 s.

**Mini-project**: **"Ghost tag"** — the Pac-grid + player + 1 chasing ghost (BFS) + dots + 1 super-pacgum: eating it makes the ghost edible (blinking) for 8 s; eating the ghost gives +200; touching a non-edible ghost costs a life and respawns you. This is VI.2 + VI.3 + VI.4 + VI.6 minus the level system.

**Explain before moving on**
- Why are timers deadlines, not sleeps? What breaks if you `sleep(2)` inside the loop?
- Describe chase vs flee with BFS on a grid. What changes in the BFS when the ghost is edible?
- When a ghost is eaten, what exact sequence of state changes happens (position, timers, score)?

**Common mistakes**
- `time.sleep` anywhere in the loop (freezes input and rendering).
- BFS recomputed with pixel coordinates instead of grid coordinates.
- Ghosts stuck forever on dead ends — ensure BFS always terminates and handle "no path" (fall back to random).
- Not resetting the edible deadline when a *second* super-pacgum is eaten.
- Reusing the player's death respawn position for ghosts (they go to their own corners, VI.3).

**Pac-Man connection**: VI.3 (ghosts: chase, flee, respawn), VI.4 (super-pacgum effect), VI.2 (lives/respawn), VI.7 (level time limit).

---

## Stage 10 — Integration prep: highscores, cheat mode, levels, config

**Concepts**
- **Highscore** (V.5): a module with load/save to JSON, robust to missing/corrupt files (try/except, default empty list), insert-sort into top-10, validate name (≤10, alnum+spaces) and score (non-negative int). Load at start, save at game end.
- **Cheat mode** (VI.5): flags/multipliers threaded through your entities: `invincible` (skip life loss), `level_skip` (jump to next level), `ghost_freeze` (skip ghost updates), `extra_lives`, `speed_multiplier`. One key toggles one cheat — a dict of key→handler.
- **Level progression** (VI.7): ≥10 levels; level 1 seed **42**, later levels random; score and lives persist across levels; each level has its own maze + timer.
- **Config** (V.2/V.3): parse JSON, strip `#` comments, clamp invalid values to defaults with a clear log message, ignore unknown keys — and take exactly one CLI arg (V.1).
- **Separation** (III + AGENTS.md): `config.py` / `maze.py` (A-Maze-ing adapter) / `entities.py` / `game.py` (state machine) / `ui.py` / `highscore.py`. Game logic never draws; rendering never mutates logic.

**APIs**: `json`, `sys.argv`, `re` for name validation, `random` for later-level seeds, `os.path` — stdlib. Pygame adds nothing new here.

**Exercises**
1. `highscore.py` with `add_score(name, score)`, top-10 trim, JSON persistence, and pytest tests for: empty file, corrupt file, name too long, score negative (III.3 expects unit tests).
2. A 3-level prototype: level 1 seed 42, levels 2–3 random; verify levels differ and score/lives carry over.
3. Wire cheat keys into the Stage 9 prototype: `I` invincible, `G` freeze ghosts, `+` extra life, `S` speed, `L` skip level.
4. Config loader: given a JSON-with-comments file, produce a dict with defaults filled; test missing/invalid keys don't crash (V.3).

**Mini-project**: **"Full prototype"** — everything from Stage 9 + 3 levels + timer + cheat keys + name entry + top-10 highscore list in the menu. This is the *entire game* minus A-Maze-ing integration and packaging.

**Explain before moving on**
- What are the exact rules for "robust" file handling in V.3 and V.5? Write the failure cases.
- How does a cheat like "ghost freeze" hook into your game loop *without* special-casing every update?
- Why must level 1 use `seed=42` and later levels use random seeds (VI.7)?

**Common mistakes**
- Crashing on a missing highscore file (V.5: must be robust).
- Not stripping `#` comments from the config before `json.loads`.
- Allowing cheat toggles to fire in menus (state leakage — Stage 7).
- Not resetting per-level state (pellets, ghost positions, timer) on level transition.
- `sys.argv` length not checked → crash with no arg (V.1: exactly one arg, clean message).

**Pac-Man connection**: V.1–V.5 (CLI, config, maze adapter, highscores), VI.5 (cheats), VI.7 (10+ levels, seed 42, persistence).

---

# Pygame topics NOT necessary for this project

| Topic | Why skip |
|---|---|
| `pygame.sprite` / `pygame.sprite.Group` | No MLX equivalent + subject demands *your own* modular OOP entities |
| `pygame.mixer` (sound/music) | Subject never mentions audio; MLX has no audio function → violates the equivalence rule. If you want sound for *fun*, keep it in a branch that's off by default. |
| `pygame.transform` (scale/rotate) | No MLX equivalent; you don't need it — all art is primitives |
| `pygame.mask` (pixel-perfect collision) | Massive overkill; rect/circle tests suffice |
| Camera / scrolling | The maze fits in one fixed window — no camera at all |
| `pygame.image` / sprite sheets | Draw everything with `draw.*`; cleaner and MLX-compatible |
| Joystick / touch / MIDI / networking | Zero relevance |
| Vector2/Vector3, physics engines | Plain tuples and `math` are enough |
| `pygame.event.post` / custom events | The state machine replaces them |

---

# "Ready for Pac-Man" checklist

**Must know** (blocking — master before coding the game):
- Game loop structure: events → update → draw → flip; what each phase is for
- Polling vs state input (`event.get` vs `key.get_pressed`) and when to use each
- Coordinate system, colors, drawing primitives, blitting
- `Rect` and the position attributes (`center`, `topleft`…)
- Time-based movement with `dt` from `time.monotonic()`, float positions, dt clamping
- Collision: `colliderect`, `collidepoint`, distance formula; move-then-check
- Text: render once/cache, blit; HUD layout (score/lives/level/time)
- The state machine: menu/pause/game-over/victory + transitions + reset
- Grid representation, grid↔pixel conversion, grid-locked movement, wall lookahead
- Deadlines (`monotonic() + t`) for timers: edible ghosts, respawn, level timer
- JSON load/save with try/except for config and highscores; `#` comment stripping; clamping

**Should know** (highly recommended):
- BFS shortest path on the grid for ghost AI (and a "no path" fallback)
- Entity classes (`Player`, `Ghost`, `Pellet`) with `update(dt)` / `draw(screen)`
- Cheat-mode design: flags + multipliers, one key per cheat, state-safe
- Pre-rendering the static maze to an off-screen Surface
- Basic debugging: `pdb` (Makefile `debug`), print-based tracing, drawing debug rects, an on-screen FPS counter
- `sys.argv` handling, `re` for name validation

**Nice to know** (optional polish):
- A custom `.ttf` font for the arcade look
- Blinking / flicker animation for edible ghosts and super-pacgums
- Performance habits: `get_size()` centering, avoiding per-pixel work, caching
- `pygame.time.Clock` purely as a dev FPS cap (keep game logic on `monotonic`)

**Not necessary** (skip, per above table): `sprite.Group`, `mixer`, `transform`, `mask`, cameras, images/sprite sheets, vectors, custom events.

---

# Recommended order to implement the actual Pac-Man project

1. **Skeleton + config**: `main.py` with CLI arg check, config loader (comments, clamping), `game.py` state machine with placeholder screens. Verify `make run`, `make lint`, `make debug` work.
2. **A-Maze-ing adapter** (`maze.py`): call the package with `PERFECT=False`, convert to your internal grid, handle generator failure cleanly.
3. **Rendering** (`render.py`): pre-render maze → off-screen Surface; draw pellets (corridors) + 4 corner super-pacgums.
4. **Player**: grid-locked movement, arrows/WASD, float positions, wall lookahead.
5. **Pellets + scoring**: collection, +10/+50, level-clear detection.
6. **Ghosts**: 4 ghosts in corners, BFS chase, then edible/flee, respawn to corner after 5–10 s, blinking.
7. **Lives + respawn**: ghost contact → −1 life, respawn center; game over at 0.
8. **Levels + timer**: ≥10 levels, seed 42 first / random later, 90 s limit, carry score/lives, victory condition.
9. **Cheat mode**: the 5 suggested cheats, bound to review-friendly keys.
10. **Highscores**: top-10 JSON module + name entry screen + menu display.
11. **UI polish**: main menu (Start/Highscores/Instructions/Exit), pause menu (Resume/Menu), game-over/victory screens with the exact flow from Chapter IV.
12. **Packaging + PM docs**: packaging script/spec, README per Chapter IX, project-management directory per Chapter VIII, `make lint` green (flake8 + mypy).

Stages 1–10 of the roadmap map 1:1 onto steps 1–11 here. If you can finish each stage's mini-projects, you will have written — piece by piece — every mechanic the subject asks for, and the real implementation becomes assembly of code you already understand and can explain during the defense.

---

