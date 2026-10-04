import pytest

from logic_utils import check_guess, update_score

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# Regression tests: hints must point the player toward the secret.
def test_too_high_guess_hints_go_lower():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message
    assert "HIGHER" not in message

def test_too_low_guess_hints_go_higher():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message
    assert "LOWER" not in message

def test_hint_direction_for_adjacent_guesses():
    assert "LOWER" in check_guess(51, 50)[1]
    assert "HIGHER" in check_guess(49, 50)[1]

def test_win_message_has_no_direction_hint():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert "HIGHER" not in message and "LOWER" not in message


# Regression tests: wrong guesses must always be penalized (Too High used to give +5 on even attempts).
@pytest.mark.parametrize("attempt_number", range(1, 9))
def test_too_high_always_loses_points(attempt_number):
    assert update_score(50, "Too High", attempt_number) == 45

@pytest.mark.parametrize("attempt_number", range(1, 9))
def test_too_low_always_loses_points(attempt_number):
    assert update_score(50, "Too Low", attempt_number) == 45

@pytest.mark.parametrize("attempt_number", range(1, 9))
def test_too_high_and_too_low_score_the_same(attempt_number):
    assert update_score(0, "Too High", attempt_number) == update_score(0, "Too Low", attempt_number)

def test_too_high_on_even_attempt_does_not_gain_points():
    assert update_score(0, "Too High", 2) < 0


# Regression tests: attempts counting and New Game reset (exercises app.py via Streamlit's AppTest).
from pathlib import Path

from streamlit.testing.v1 import AppTest

APP_PATH = str(Path(__file__).resolve().parent.parent / "app.py")


def _new_app():
    at = AppTest.from_file(APP_PATH)
    at.run()
    assert not at.exception
    return at


def _button(at, label_part):
    return next(b for b in at.button if label_part in b.label)


def _guess(at, value):
    at.text_input[0].set_value(str(value))
    _button(at, "Submit").click()
    at.run()
    assert not at.exception


def _new_game(at):
    _button(at, "New Game").click()
    at.run()
    assert not at.exception


def test_attempts_start_at_zero():
    at = _new_app()
    assert at.session_state.attempts == 0


def test_first_guess_counts_as_attempt_one():
    at = _new_app()
    at.session_state.secret = 50
    _guess(at, 10)
    assert at.session_state.attempts == 1


def test_new_game_resets_attempts_to_zero():
    at = _new_app()
    at.session_state.secret = 50
    _guess(at, 10)
    _guess(at, 20)
    assert at.session_state.attempts == 2
    _new_game(at)
    assert at.session_state.attempts == 0


def test_new_game_clears_history_and_score():
    at = _new_app()
    at.session_state.secret = 50
    _guess(at, 10)
    assert at.session_state.history == [10]
    assert at.session_state.score != 0
    _new_game(at)
    assert at.session_state.history == []
    assert at.session_state.score == 0


def test_new_game_after_loss_returns_to_playing():
    at = _new_app()
    at.session_state.secret = 50
    at.session_state.attempts = 7  # Normal allows 8
    _guess(at, 10)
    assert at.session_state.status == "lost"
    _new_game(at)
    assert at.session_state.status == "playing"
    assert at.session_state.attempts == 0


def test_new_game_after_win_returns_to_playing():
    at = _new_app()
    at.session_state.secret = 50
    _guess(at, 50)
    assert at.session_state.status == "won"
    _new_game(at)
    assert at.session_state.status == "playing"


# Regression tests: the secret used to be cast to a str on even attempts, breaking check_guess.
def _guess_on_attempt(secret, guess, attempt_number):
    at = _new_app()
    at.session_state.secret = secret
    at.session_state.attempts = attempt_number - 1
    _guess(at, guess)
    assert at.session_state.attempts == attempt_number
    return at


@pytest.mark.parametrize("attempt_number", range(1, 9))
def test_correct_guess_wins_on_any_attempt(attempt_number):
    at = _guess_on_attempt(50, 50, attempt_number)
    assert at.session_state.status == "won"


@pytest.mark.parametrize("attempt_number", [2, 4, 6])
def test_numeric_comparison_on_even_attempts(attempt_number):
    # Lexicographically "9" > "50", so a str secret would wrongly report Too High.
    at = _guess_on_attempt(50, 9, attempt_number)
    assert "HIGHER" in at.warning[0].value
    assert "LOWER" not in at.warning[0].value


@pytest.mark.parametrize("attempt_number", [1, 2, 3, 4])
def test_hint_matches_check_guess_on_every_attempt(attempt_number):
    for guess in (9, 100):
        at = _guess_on_attempt(50, guess, attempt_number)
        # Streamlit lifts the leading emoji into the icon, so compare the text only.
        assert at.warning[0].value in check_guess(guess, 50)[1]


def test_secret_stays_an_int_after_even_attempt():
    at = _guess_on_attempt(50, 10, 2)
    assert isinstance(at.session_state.secret, int)


def test_new_game_secret_respects_difficulty_range():
    at = _new_app()
    at.sidebar.selectbox[0].set_value("Easy")
    at.run()
    for _ in range(30):
        _new_game(at)
        assert 1 <= at.session_state.secret <= 20
