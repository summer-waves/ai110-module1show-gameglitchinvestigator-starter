# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit. It wrote the code, ran away, and now the game is unplayable.

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🔧 Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the fixed app: `python -m streamlit run app.py`

## 🕵️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"?
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] Describe the game's purpose.
- [x] Detail which bugs you found.
- [x] Explain what fixes you applied.

### Game Purpose
This is a number guessing game where the player tries to guess a secret number within a limited number of attempts. After each guess, the game gives a hint telling the player whether to guess higher or lower. Points are awarded for winning and deducted for wrong guesses.

### Bugs Found
| # | Bug | Location | Impact |
|---|-----|----------|--------|
| 1 | Hints inverted ("Go HIGHER" when guess is too high) | `check_guess` in `app.py` | Player is actively misled on every wrong guess |
| 2 | Secret randomly cast to string on even attempts | `app.py` submit block | Comparisons break every other turn; win is impossible |
| 3 | Wrong guesses award points on even attempts | `update_score` in `app.py` | Score is unreliable and rewards bad play |
| 4 | Hard mode range (1–50) easier than Normal (1–100) | `get_range_for_difficulty` | Difficulty labels are misleading |
| 5 | Attempts counter inconsistent between init and new game | `app.py` session state init | Off-by-one in attempts display |

### Fixes Applied
- Swapped the hint messages in `check_guess` so "Too High" → "Go LOWER" and "Too Low" → "Go HIGHER"
- Removed the odd/even branching that converted the secret to a string; `secret` is always an int now
- Simplified `update_score` so all non-winning outcomes deduct points consistently
- Corrected Hard mode range to `1–200` (harder than Normal)
- Standardized attempts counter to start at `0` in both init and new game reset
- Refactored all game logic from `app.py` into `logic_utils.py`
- Updated the info message to show the actual difficulty range instead of always saying "1 to 100"

## 📸 Demo

> Replace this line with a screenshot of your fixed, winning game.

## 🚀 Stretch Features

> (Optional) Replace this line with a screenshot of your enhanced UI if you completed Challenge 4.