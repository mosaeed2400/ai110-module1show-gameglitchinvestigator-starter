# FIX: Refactored all game logic from app.py into this file using Claude Code


def get_range_for_difficulty(difficulty: str):
    """Return the inclusive guessing range for a difficulty level.

    Args:
        difficulty: The difficulty name. Recognized values are
            "Easy", "Normal", and "Hard".

    Returns:
        A ``(low, high)`` tuple of ints describing the inclusive range
        of valid secret numbers. Unrecognized values fall back to the
        "Normal" range of ``(1, 100)``.
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str):
    """Parse raw user input into an integer guess.

    Accepts plain integer strings (e.g. ``"42"``) as well as decimal
    strings (e.g. ``"42.9"``), which are truncated toward zero via
    ``int(float(raw))``.

    Args:
        raw: The unparsed input string from the user. May be ``None``
            or empty.

    Returns:
        A 3-tuple ``(ok, guess_int, error_message)`` where:

        * ``ok`` (bool): ``True`` if parsing succeeded.
        * ``guess_int`` (int | None): The parsed integer, or ``None``
          on failure.
        * ``error_message`` (str | None): A human-readable error, or
          ``None`` on success.
    """
    if raw is None:
        return False, None, "Enter a guess."
    if raw == "":
        return False, None, "Enter a guess."
    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."
    return True, value, None


def check_guess(guess, secret):
    """Compare a guess against the secret number and return a hint.

    Args:
        guess: The player's guess. Normally an int, but the function
            guards against type mismatches (see below).
        secret: The secret number to compare against.

    Returns:
        A ``(outcome, message)`` tuple where ``outcome`` is one of
        ``"Win"``, ``"Too High"``, or ``"Too Low"``, and ``message`` is
        an emoji-prefixed hint directing the player higher or lower.

    Note:
        If comparing ``guess`` and ``secret`` raises ``TypeError``
        (e.g. mismatched types), the guess is coerced to a string and
        compared lexicographically as a fallback. This fallback path is
        a last resort and does not perform numeric comparison.
    """
    if guess == secret:
        return "Win", "🎉 Correct!"
    try:
        if guess > secret:
            return "Too High", "📉 Go LOWER!"
        else:
            return "Too Low", "📈 Go HIGHER!"
    except TypeError:
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        if g > secret:
            return "Too High", "📉 Go LOWER!"
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Compute the new score after a guess.

    A win awards ``100 - 10 * (attempt_number + 1)`` points, floored at
    a minimum of 10 points so later wins still score something. A
    "Too High" outcome adds 5 points on even attempt numbers and
    subtracts 5 otherwise; a "Too Low" outcome always subtracts 5.

    Args:
        current_score: The player's score before this guess.
        outcome: The result from :func:`check_guess` ("Win",
            "Too High", or "Too Low").
        attempt_number: The 1-based count of attempts made so far.

    Returns:
        The updated score as an int. Unrecognized outcomes leave the
        score unchanged.
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points
    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5
    if outcome == "Too Low":
        return current_score - 5
    return current_score
