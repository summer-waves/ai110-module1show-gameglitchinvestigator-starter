from logic_utils import check_guess, parse_guess, get_range_for_difficulty, update_score

# --- check_guess tests ---

def test_winning_guess():
    result, _ = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # Guess of 60 against secret of 50 should be Too High
    result, _ = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # Guess of 40 against secret of 50 should be Too Low
    result, _ = check_guess(40, 50)
    assert result == "Too Low"

def test_hint_message_too_high():
    # When guess is too high, message should say go LOWER (not higher)
    _, msg = check_guess(80, 50)
    assert "LOWER" in msg

def test_hint_message_too_low():
    # When guess is too low, message should say go HIGHER (not lower)
    _, msg = check_guess(20, 50)
    assert "HIGHER" in msg

# --- parse_guess tests ---

def test_parse_valid_integer():
    ok, val, err = parse_guess("42")
    assert ok is True
    assert val == 42
    assert err is None

def test_parse_empty_string():
    ok, val, err = parse_guess("")
    assert ok is False
    assert err == "Enter a guess."

def test_parse_none():
    ok, val, err = parse_guess(None)
    assert ok is False

def test_parse_decimal_truncates():
    ok, val, err = parse_guess("7.9")
    assert ok is True
    assert val == 7

def test_parse_non_numeric():
    ok, val, err = parse_guess("abc")
    assert ok is False
    assert err == "That is not a number."

# --- get_range_for_difficulty tests ---

def test_easy_range():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1 and high == 20

def test_normal_range():
    low, high = get_range_for_difficulty("Normal")
    assert low == 1 and high == 100

def test_hard_range_is_harder_than_normal():
    _, hard_high = get_range_for_difficulty("Hard")
    _, normal_high = get_range_for_difficulty("Normal")
    assert hard_high > normal_high

# --- update_score tests ---

def test_win_adds_points():
    new_score = update_score(0, "Win", 1)
    assert new_score > 0

def test_wrong_guess_deducts_points():
    score_after_high = update_score(50, "Too High", 2)
    score_after_low = update_score(50, "Too Low", 3)
    assert score_after_high < 50
    assert score_after_low < 50