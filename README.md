# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] The game is a number guessing game where the player guesses a number between 1 and 100.
- [x] Bugs found: backwards hints, New Game not resetting status, attempts starting at 1, secret converted to string on even attempts.
- [x] Fixed hints logic, reset status on New Game, set attempts to 0, removed string conversion bug.

## 📸 Demo Walkthrough

1. Run the app with `python3 -m streamlit run app.py`
2. Open the Developer Debug Info tab to see the secret number
3. Type a number lower than the secret — hint correctly says "Go HIGHER"
4. Type a number higher than the secret — hint correctly says "Go LOWER"
5. Type the exact secret number — game shows "Correct!" and you win
6. Click New Game — game fully resets with a new secret number

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
python3 -m pytest tests/
................
16 passed in 0.03s
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
