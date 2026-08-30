## 1. Understanding the General Game Flow (Lifecycle)

- I read the project subject and studied the game's interactions and logic to fully understand the scope of the project.
- Based on this, I designed the general Pac-Man game flow:

### Game Lifecycle
`Main Menu` ➔ `Start Game` ➔ `Win or Lose` ➔ `Enter Name for Highscore` ➔ `Back to Main Menu`

**1. Main Menu**
* Display the Main Menu screen.
* Load the high score file to display current records.
* Pressing `SPACE` transitions the user to the Play Game screen.

**2. Start Game**
* Load the configuration sequentially (Level 1, Level 2, etc.).
* Display the Play Game screen.
* Continuously render the updated map based on backend state changes.

**3. Win or Lose**
* Display specific screens depending on the game outcome.
* Prompt the player to enter their name for the high score board in both scenarios.

**4. Back to Main Menu**
* Restart the game loop entirely.

### UI Rendering
The Play Game screen is refreshed and redrawn under two conditions:
1. **User Input:** When the player registers a keystroke.
2. **Backend Updates:** When internal game state changes occur on a timer (e.g., ghosts move, Pac-Man moves).

---

## 2. Managing the Configuration File (Path, Permissions, Loading, and Errors)

- I am responsible for loading, validating, and applying the game's configuration. This includes retrieving a valid file path, checking read permissions, verifying file existence, and ensuring the JSON format is valid.
- To comply with the strict project requirement of never crashing with a Python traceback, I implemented a robust fallback system. If invalid or corrupted configuration values are provided, the program automatically clamps to safe default values and prints clear, visible warning messages (preventing both silent errors and hard crashes).

---

## 4- The Make file

## 5- Highscore file Management

## 3. The Shape of the Grid Representing the Game Backend

*(Content pending...)*