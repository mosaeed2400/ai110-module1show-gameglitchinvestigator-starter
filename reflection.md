# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When I first ran the game, it loaded in the browser but immediately had issues. 
The hints were backwards — guessing lower than the secret number showed "Go LOWER" 
instead of "Go HIGHER". After winning, clicking New Game still showed "You already 
won" and blocked play. The score went negative after normal guesses due to broken 
scoring logic. The attempts counter also started at 1 instead of 0.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess of 20, secret is 63 | Hint says "Go HIGHER" | Hint says "Go LOWER" | none |
| Click New Game after winning | Game fully resets, won message clears | "You already won" message still shows | none |
| Any wrong guess submitted | Score stays at 0 or decreases by 1 | Score drops to -5 immediately | none |

---

## 2. How did you use AI as a teammate?

I used Claude (claude.ai) and Claude Code in VS Code as my AI tools on this project. Claude Code read both app.py and logic_utils.py and correctly explained that the backwards hints bug lived in the check_guess function — both in the main path and the except TypeError fallback. I verified this by testing the game manually and confirming the hints were wrong before and correct after the fix. One example where AI was helpful was when it identified the string conversion bug on even attempts, which I had not noticed myself. One example where I had to use my own judgment was fixing the test file — the AI-generated starter tests were written incorrectly, asserting against a string instead of unpacking the tuple, so I had to understand the code and fix the tests myself.

---

## 3. Debugging and testing your fixes

I decided a bug was really fixed when the game behaved correctly manually AND the pytest tests passed. For example, after fixing the hints, I tested by guessing 30 when the secret was 39 and confirmed it said "Go HIGHER" correctly. I then ran `python3 -m pytest tests/` and got 3 passed, which confirmed the fix was solid. Claude Code helped me understand why the tests were failing — it explained that check_guess returns a tuple, so the tests needed to unpack it with `outcome, message = check_guess(...)` instead of just `result = check_guess(...)`.

---

## 4. What did you learn about Streamlit and state?

Streamlit reruns the entire Python script from top to bottom every time a user clicks a button or interacts with the app. This means any regular variable gets reset to its original value on every click. Session state (`st.session_state`) is like a special dictionary that survives these reruns — so storing the secret number there keeps it from changing every time the user clicks Submit.

---

## 5. Looking ahead: your developer habits

One habit I want to reuse is testing manually first to observe bugs, then writing pytest cases to confirm fixes — that combination gave me confidence the code was truly fixed. Next time I work with AI on a coding task, I would read the AI-generated code more carefully before running it, instead of assuming it is correct. This project changed my thinking because I now understand that AI-generated code can look clean and professional but still contain subtle logic bugs that only show up when you actually run and test it.
