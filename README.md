# Rock-Paper-Scissors (Python)

This repository contains a solution to the JetBrains Hyperskill project "Rock-Paper-Scissors" (also the extended "Rock-Paper-Scissors-Lizard-Spock" style with customizable options). The implementation is a console-based Python game that supports:

- Standard 3-option mode: rock, paper, scissors
- Custom mode: any odd-numbered list of options provided by the user (e.g., "rock,fire,scissors,lizard,spock")
- Persistent rating system backed by a `rating.txt` file
- Commands:
  - `!exit` — quit the game
  - `!rating` — show the player's current rating

This solution follows the rules and expected behavior from the Hyperskill project.

## Files

- `game.py` (or the single script containing the game logic) — the game implementation (see code in the repository).
- `rating.txt` — a plain text file storing player names and their scores; created/updated by the game.

## How it works (high level)

- On start the program asks for your name.
- It reads `rating.txt` (if present) and initializes your rating (0 if not found).
- Then the program reads a single line of user input that defines the game options. If the line is empty, the default `["scissors", "paper", "rock"]` is used.
  - Example empty input: classic mode
  - Example custom input: `rock,gun,lightning,devil,dragon,water,air,paper,sponge`
- The program prints `Okay, let's start` and waits for repeated user moves.
- Valid moves are any of the game options, plus `!exit` and `!rating`.
- Game result and rating points:
  - Draw: +50 points
  - Win: +100 points
  - Loss: 0 points
- For the classic 3-option mode, the program uses a fixed winning map:
  - scissors beats paper
  - rock beats scissors
  - paper beats rock
- For custom lists of N options (N must be odd for the usual circular logic), the program computes which choices beat which using circular ordering:
  - For the chosen option, the next N//2 options (wrapping around) beat it; the remaining options are the ones it beats.
- Ratings are stored (and updated) in `rating.txt` so they persist between runs.

## Example usage

1. Start the program:
   - python main.py
2. Enter your name when prompted:
   - Enter your name: Alice
3. Enter game options (comma-separated), or press Enter for classic mode:
   - (press Enter)  -> classic mode
   - or: rock,paper,scissors,lizard,spock
4. Play by typing one move per line:
   - rock
   - !rating
   - !exit

Example session:
- Hello, Alice
- (input) [enter] -> "Okay, let's start"
- (input) rock -> "Well done. The computer chose scissors and failed" (and +100 points saved)
- (input) !rating -> "Your rating: 150"
- (input) !exit -> "Bye!"

## Notes about implementation details

- Usernames are normalized with capitalization; comparison to existing ratings is case-insensitive.
- `rating.txt` is read and written in plain UTF-8 text. Each line is: `<Name> <score>`
- When a new user plays, the program appends an initial line with score 0 to `rating.txt`.
- The program ensures only allowed inputs are accepted — invalid inputs produce the message `Invalid input`.
- The code uses a deterministic circular algorithm for custom option lists so that the game is fair for any odd-length list of elements.

## Extending or modifying

- To change point values, edit the `POINTS` mapping in the script.
- To persist ratings in a different format (JSON, DB, etc.), replace reading/writing logic around `rating.txt`.
- To add more commands, extend the `OTHER_OPTIONS` constant and handle logic in the main loop.

## License & Credits

This repository contains a learning exercise solution inspired by JetBrains Hyperskill (project link):
https://hyperskill.org/projects/78

Author: Balick (GitHub: @Balick)
Hyperskill profile referenced in the original README: https://hyperskill.org/profile/386978127

Feel free to reuse or adapt this implementation for learning purposes.
