from logic_utils import check_guess, parse_guess


# ---------------------------------------------------------------------------
# check_guess: baseline behavior
# ---------------------------------------------------------------------------

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"


# ---------------------------------------------------------------------------
# parse_guess: edge cases
# ---------------------------------------------------------------------------

def test_parse_negative_number():
    # Negative integers are valid input and parse straight through.
    ok, value, err = parse_guess("-5")
    assert ok is True
    assert value == -5
    assert err is None


def test_parse_decimal_truncates_toward_zero():
    # Decimals are accepted and truncated via int(float(...)).
    ok, value, err = parse_guess("42.9")
    assert ok is True
    assert value == 42
    assert err is None


def test_parse_negative_decimal_truncates_toward_zero():
    # Truncation toward zero means -3.7 becomes -3, not -4.
    ok, value, err = parse_guess("-3.7")
    assert ok is True
    assert value == -3
    assert err is None


def test_parse_very_large_number():
    # Python ints are unbounded, so huge integer strings parse exactly.
    big = "100000000000000000000"  # 10**20
    ok, value, err = parse_guess(big)
    assert ok is True
    assert value == 10 ** 20
    assert err is None


def test_parse_large_scientific_notation():
    # Scientific notation contains '.', so it routes through float() first.
    ok, value, err = parse_guess("1.5e3")
    assert ok is True
    assert value == 1500
    assert err is None


# ---------------------------------------------------------------------------
# check_guess: edge cases
# ---------------------------------------------------------------------------

def test_check_negative_guess_below_secret():
    # A negative guess is below a positive secret -> too low.
    outcome, message = check_guess(-5, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message


def test_check_guess_above_negative_secret():
    # Comparison still works when the secret itself is negative.
    outcome, message = check_guess(50, -5)
    assert outcome == "Too High"
    assert "LOWER" in message


def test_check_matching_negative_values_win():
    outcome, message = check_guess(-7, -7)
    assert outcome == "Win"


def test_check_decimal_guess_above_secret():
    # check_guess can receive a float directly (not just parsed ints).
    outcome, message = check_guess(50.5, 50)
    assert outcome == "Too High"
    assert "LOWER" in message


def test_check_decimal_guess_below_secret():
    outcome, message = check_guess(49.5, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message


def test_check_very_large_guess_above_secret():
    outcome, message = check_guess(10 ** 18, 50)
    assert outcome == "Too High"
    assert "LOWER" in message


def test_check_very_large_secret_above_guess():
    outcome, message = check_guess(50, 10 ** 18)
    assert outcome == "Too Low"
    assert "HIGHER" in message


def test_check_matching_very_large_values_win():
    outcome, message = check_guess(10 ** 18, 10 ** 18)
    assert outcome == "Win"
