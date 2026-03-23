# 💭 Reflection: Game Glitch Investigator

## 1. What was broken when you started?

When I first ran the game, it looked functional on the surface — the UI loaded, I could type a guess and hit Submit — but it quickly became clear something was deeply wrong. The hints were giving me the opposite advice: when I guessed too high, it told me to go higher, and when I guessed too low, it told me to go lower. It was impossible to win by following the hints. I also noticed the score was going up even when I guessed wrong on certain turns, which felt backwards. Additionally, the "Hard" difficulty was labeled harder but its range (1–50) was actually smaller and easier than Normal (1–100), and the info message always said "Guess between 1 and 100" regardless of which difficulty was selected.

**Bug 1 — Inverted hints:** In `check_guess`, the messages were swapped. A guess that was too high displayed "📈 Go HIGHER!" and a guess that was too low displayed "📉 Go LOWER!" — the exact opposite of what they should say.

**Bug 2 — Secret number randomly becomes a string:** Every other attempt, the code converted the secret number to a string before comparing it to the player's integer guess. This caused comparisons like `40 > "50"` which behave unpredictably in Python, making it nearly impossible to get a correct result on even-numbered attempts.

**Bug 3 — Score increases on wrong guesses:** The `update_score` function had a branch that awarded +5 points whenever the guess was "Too High" on an even-numbered attempt. Wrong guesses should never reward points.

---

## 2. How did you use AI as a teammate?

I used GitHub Copilot (via VS Code) throughout this project for code explanation, refactoring suggestions, and test generation.

**Correct suggestion:** When I asked Copilot to explain the `check_guess` function step by step, it correctly identified that the hint messages were inverted — "Go HIGHER" and "Go LOWER" were assigned to the wrong branches of the if/else. I verified this by manually tracing through the logic: if `guess > secret`, the guess is too high, so the player should go lower. The original code said the opposite. After swapping the messages, I ran the pytest suite and the `test_hint_message_too_high` and `test_hint_message_too_low` tests both passed.

**Incorrect/misleading suggestion:** When I asked Copilot to fix the string/integer comparison bug, it initially suggested wrapping the guess in `str()` before comparing, so both sides would be strings. This was misleading — it would have "fixed" the crash but broken correct comparisons (e.g., `"9" > "50"` is `True` in Python due to lexicographic ordering). I rejected this and instead fixed the root cause by removing the odd/even branching that converted the secret to a string in the first place.

---

## 3. Debugging and testing your fixes

I decided a bug was truly fixed only when both conditions were met: the pytest test for that specific behavior passed, and the live Streamlit game behaved correctly when I played it manually. Passing tests alone weren't enough — I wanted to confirm the fix felt right in the actual UI too.

For the inverted hints bug, I wrote `test_hint_message_too_high` and `test_hint_message_too_low` in `test_game_logic.py`. These tests call `check_guess` directly and assert that the returned message contains "LOWER" when the guess is too high, and "HIGHER" when the guess is too low. Before the fix both tests failed; after swapping the messages they passed immediately.

Copilot helped me design the edge-case tests, particularly the ones for `parse_guess` — it suggested testing `None`, empty string, and decimal inputs, which I hadn't initially thought to cover. I reviewed each suggestion and kept the ones that matched real scenarios a player might accidentally trigger.

---

## 4. What did you learn about Streamlit and state?

Every time a user interacts with a Streamlit app — clicking a button, typing in a box, changing a dropdown — Streamlit re-runs the entire Python script from the top. Think of it like refreshing a webpage, except it happens automatically on every interaction. The problem is that any regular Python variable you set gets wiped out on each re-run, which is why the secret number kept changing every time the Submit button was clicked in the buggy version.

`st.session_state` is Streamlit's solution to this problem. It's a special dictionary that persists across re-runs for the duration of the user's session. By storing the secret number, attempt count, score, and game status in `st.session_state`, those values survive re-runs and the game can track progress correctly. The pattern `if "secret" not in st.session_state: st.session_state.secret = ...` ensures we only initialize a value once, and then leave it alone on subsequent re-runs.

---

## 5. Looking ahead: your developer habits

One habit I want to carry forward is writing tests that target the *specific behavior* that was broken — not just generic "does it run" tests. For example, writing `test_hint_message_too_high` to assert the word "LOWER" appears in the message is much more useful than just checking that `check_guess` returns something. This kind of focused, behavior-driven test makes bugs hard to reintroduce accidentally.

Next time I work with AI on a coding task, I would be more skeptical of fixes that treat a symptom rather than the root cause. Copilot's suggestion to convert the guess to a string would have silenced the error without actually fixing the logic — a good reminder to always ask "why does this fix it?" before accepting a suggestion.

This project changed how I think about AI-generated code by showing me that AI can produce code that looks completely reasonable and runs without crashing, but still has subtle logic errors that only show up during real use. AI is a fast first draft, not a finished product.