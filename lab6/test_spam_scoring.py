import pytest
from spam_scoring import score_message, classify, filter_inbox, inbox_status

# ==============================================================================
# Code Coverage Test Suite (Statement Coverage Analysis)
# Focus: Ensure every line of executable code in spam_scoring.py is reached.
# ==============================================================================

def test_plain_message_scores_zero():
    assert score_message("hello there", False, 0) == 0

def test_low_score_is_clean():
    assert classify(1) == "clean"

def test_score_message_spam_words_and_many_links():
    # Covers: spam words (line 8), link_count > 3 (line 12)
    score = score_message("free prize cash", False, 4)
    assert score == 10

def test_score_message_uppercase_and_sender_known_clamp():
    # Covers: uppercase > 3 (line 10), link_count > 0 (line 14), sender_known with score < 0 (lines 16-18)
    score = score_message("HELLO", True, 1)
    assert score == 0

def test_classify_all_levels():
    # Covers: score >= 8 (line 24), score >= 4 (line 26), else (line 27)
    assert classify(9) == "spam"
    assert classify(5) == "suspicious"
    assert classify(1) == "clean"

def test_filter_inbox():
    # Covers: inbox filtering loop and classification counting (lines 31-35)
    msgs = [
        ("free urgent prize", False, 4),
        ("hello friend", False, 0)
    ]
    counts = filter_inbox(msgs)
    assert counts["spam"] == 1
    assert counts["clean"] == 1
    assert counts["suspicious"] == 0

def test_inbox_status_all_outcomes():
    # Covers: total == 0 (line 41), ratio > 0.5 (line 44), ratio > 0.2 (line 46), else healthy (line 47)
    assert inbox_status({"spam": 0, "suspicious": 0, "clean": 0}) == "empty"
    assert inbox_status({"spam": 3, "suspicious": 0, "clean": 1}) == "flooded"
    assert inbox_status({"spam": 1, "suspicious": 0, "clean": 2}) == "noisy"
    assert inbox_status({"spam": 0, "suspicious": 1, "clean": 3}) == "healthy"
