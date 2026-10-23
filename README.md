# Pac-Man

A Pac-Man clone written in Python with [pygame](https://www.pygame.org/). Each game takes place in a procedurally generated maze. Four ghosts chase you, and each one has its own targeting behaviour based on the original arcade game.

## Features

- **Procedurally generated mazes**: built with the bundled `mazegenerator` package. A seed makes the layout reproducible.
- **Four ghosts with distinct AI**:
  - **Blinky** (red) targets Pac-Man's current tile.
  - **Pinky** (pink) targets the tile four squares in front of Pac-Man.
  - **Inky** (light blue) targets the point you get by mirroring Blinky's position through Pac-Man.
  - **Clyde** (orange) chases like Blinky when far away and retreats to scatter mode when within 8 tiles.
- **Ghost modes**: scatter and chase alternate (about 6 s and 5 s). Eating a super pacgum puts the ghosts into frightened mode for about 10 s. Eaten ghosts go back to their origin.
- **Multiple levels** and a per-level countdown timer.
- **High-score table**: after a game you can enter your name, and the top 10 scores appear on the main menu.
- **Fullscreen display**: cell size scales automatically to fit your screen.

## Requirements

- Python 3.10+
- pygame 2.6.1
- `mazegenerator` (included as `mazegenerator-00001-py3-none-any.whl`)

## Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

`requirements.txt` installs both pygame and the local `mazegenerator` wheel.

## Running

```bash
make run
# or
python3 pac-man.py [config.json]
```

If you don't pass a config file, `config.json` is used.

## Controls

| Key | Action |
| --- | --- |
| `W` `A` `S` `D` / arrow keys | Move |
| `Space` | Start a new game (main menu) |
| `I` | Show instructions (main menu) |
| `Esc` | Pause/resume during play, go back from menus, quit from the main menu |
| `↑` `↓` + `Enter` | Navigate the pause menu |

### Debug keys (during play)

| Key | Action |
| --- | --- |
| `P` | Freeze/unfreeze the ghosts |
| `B` | Toggle Pac-Man speed boost |
| `I` | Toggle infinite lives |

## Gameplay

- Eat every pacgum in the maze to clear the level. Clear the last level to win.
- The four corners hold **super pacgums**. Eating one makes the ghosts frightened, and while they are frightened you can eat them for bonus points.
- Touching a normal ghost costs a life. The game ends when you run out of lives or the level timer reaches zero.
- When the game ends, whether you won or lost, you can enter a name to save your score.

## Configuration

Game settings come from a JSON file (`config.json` by default). Lines starting with `#` or `//` are treated as comments. Unknown keys are ignored. If a value is missing or out of range, the default is used instead.

| Key | Description | Valid range | Default |
| --- | --- | --- | --- |
| `highscore_filename` | Path to the high-score JSON file | writable `.json` path | `highscores.json` |
| `levels` | Number of levels | 1–20 | 10 |
| `width` | Maze width in cells | 15–35 | 15 |
| `height` | Maze height in cells | 15–35 | 15 |
| `lives` | Starting lives | 1–8 | 3 |
| `pacgum` | Number of pacgums per level | 42 – (width × height − 26) | 42 |
| `points_per_pacgum` | Points per pacgum | 0–50 | 10 |
| `points_per_super_pacgum` | Points per super pacgum | 0–100 | 50 |
| `points_per_ghost` | Points per eaten ghost | 0–1000 | 200 |
| `seed` | Maze generation seed (int or float) | any number | 42 |
| `level_max_timer` | Seconds allowed per level | 90–240 | 90 |

Example (`config.json`):

```json
{
    "highscore_filename": "highscore.json",
    "levels": 10,
    "width": 15,
    "height": 15,
    "lives": 3,
    "pacgum": 42,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "seed": 42,
    "level_max_timer": 240
}
```

`back_end/default_config.json` is deliberately full of invalid values. Run the game with it to test that the config validation falls back to the defaults correctly.

## Project structure

```
pac_man/
├── pac-man.py            # Entry point: game loop and state machine
├── screen_renders.py     # Main menu, maze rendering, pause, win/lose screens
├── TextInputBox.py       # Name input widget for the high-score table
├── config.json           # Game configuration
├── Makefile              # run / lint targets
├── requirements.txt
├── assets/
│   ├── player_images/    # Pac-Man animation frames
│   └── ghost_images/     # Ghost sprites (normal, frightened, eaten)
└── back_end/
    ├── Maze.py           # Game manager: maze, pacgums, collisions, levels
    ├── PacMan.py         # Player movement, score, lives
    ├── Ghost.py          # Shared ghost logic and modes
    ├── Blinky.py / Pinky.py / Inky.py / Clyde.py
    ├── config_parser.py  # JSON config loading and validation
    └── constants.py      # Screen and cell-size setup
```

## Development

Run the linters:

```bash
make lint
```

This runs `flake8` and `mypy` in strict mode (`--disallow-untyped-defs`, `--check-untyped-defs`).
