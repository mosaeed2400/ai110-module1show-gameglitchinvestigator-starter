import random
import streamlit as st
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score
# FIX: Refactored all game logic into logic_utils.py using Claude Code

# Color-code hints by outcome: Too High = red, Too Low = blue, Win = green.
HINT_COLORS = {
    "Win": "green",
    "Too High": "red",
    "Too Low": "blue",
}


def render_hint(outcome, message):
    """Display a hint message colored according to its outcome."""
    color = HINT_COLORS.get(outcome, "gray")
    st.markdown(f"### :{color}[{message}]")


def render_summary():
    """Render a table of every guess this session and its outcome."""
    if st.session_state.get("rounds"):
        st.divider()
        st.subheader("📊 Session Summary")
        st.table(st.session_state.rounds)


def render_guess_history_sidebar():
    """Show a sidebar bar chart of how far each guess was from the secret.

    Only numeric (valid) guesses are charted; invalid entries are skipped.
    Bar height is the absolute distance from the secret, so shorter bars
    mean the guess was closer.
    """
    valid = [
        r for r in st.session_state.get("rounds", [])
        if r["Outcome"] != "Invalid"
    ]
    if not valid:
        return

    secret = st.session_state.secret
    distances = [abs(r["Guess"] - secret) for r in valid]
    labels = [f"#{r['Attempt']}" for r in valid]

    st.sidebar.divider()
    st.sidebar.subheader("📊 Guess History")
    st.sidebar.caption("Distance from secret (shorter = closer)")
    st.sidebar.bar_chart({"label": labels, "Distance": distances}, x="label")


st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

# FIX: Changed attempts starting value from 1 to 0 — was causing attempts counter to be off by one
if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

# Records of each round (attempt #, guess, outcome) for the summary table.
if "rounds" not in st.session_state:
    st.session_state.rounds = []

st.subheader("Make a guess")

st.info(
    f"Guess a number between 1 and 100. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

# FIX: Added status and history reset so New Game clears the won/lost state
if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(1, 100)
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.rounds = []
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    render_guess_history_sidebar()
    render_summary()
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.session_state.rounds.append({
            "Attempt": st.session_state.attempts,
            "Guess": raw_guess,
            "Outcome": "Invalid",
        })
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        # FIX: Removed string conversion bug that broke comparisons on even attempts
        secret = st.session_state.secret

        outcome, message = check_guess(guess_int, secret)

        st.session_state.rounds.append({
            "Attempt": st.session_state.attempts,
            "Guess": guess_int,
            "Outcome": outcome,
        })

        if show_hint:
            render_hint(outcome, message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

render_guess_history_sidebar()
render_summary()

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")