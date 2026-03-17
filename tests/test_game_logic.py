from logic_utils import check_guess

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

# Tests targeting the backwards hint bug:
# The bug caused "Go HIGHER!" when the guess was too high,
# and "Go LOWER!" when the guess was too low — the opposite of correct.

def test_too_high_message_says_go_lower():
    # Guess (70) is above secret (50), so the hint must say Go LOWER
    outcome, message = check_guess(70, 50)
    assert outcome == "Too High"
    assert "LOWER" in message, f"Expected 'LOWER' in hint but got: '{message}'"

def test_too_low_message_says_go_higher():
    # Guess (30) is below secret (50), so the hint must say Go HIGHER
    outcome, message = check_guess(30, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message, f"Expected 'HIGHER' in hint but got: '{message}'"

def test_too_high_message_does_not_say_go_higher():
    # Regression guard: the old buggy message "Go HIGHER!" must not appear when guess is too high
    outcome, message = check_guess(70, 50)
    assert "HIGHER" not in message, f"Backwards hint bug detected: got '{message}' for a too-high guess"

def test_too_low_message_does_not_say_go_lower():
    # Regression guard: the old buggy message "Go LOWER!" must not appear when guess is too low
    outcome, message = check_guess(30, 50)
    assert "LOWER" not in message, f"Backwards hint bug detected: got '{message}' for a too-low guess"

def test_close_guess_below_teens_secret_is_too_low():
    # Regression guard for the string-secret bug in app.py:
    # When secret was cast to str on even attempts, lexicographic comparison
    # made "9" > "10" evaluate to True, incorrectly returning "Too High".
    # A guess of 9 with secret 10 must be "Too Low", not "Too High".
    outcome, message = check_guess(9, 10)
    assert outcome == "Too Low", f"Expected 'Too Low' but got '{outcome}' — string comparison bug may have returned wrong direction"
    assert "HIGHER" in message
