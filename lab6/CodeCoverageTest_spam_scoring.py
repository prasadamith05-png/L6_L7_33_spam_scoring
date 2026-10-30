import pytest
from spam_scoring import score_message, classify, filter_inbox, inbox_status

# ==============================================================================
# Code Coverage Test Suite (Statement Coverage Analysis)
# Focus: Ensure every line of executable code in spam_scoring.py is reached.
# ==============================================================================

def test_score_message_spam_words_and_many_links():
    """
    Covers lines in score_message:
    - line 7, 8: SPAM_WORDS detection (+2 per word)
    - line 11, 12: link_count > 3 (+4)
    """
    score = score_message("free prize cash", False, 4)
    # 3 spam words (3 * 2 = 6) + links (>3 -> 4) = 10
    assert score == 10


def test_score_message_uppercase_and_sender_known_clamp():
    """
    Covers lines in score_message:
    - line 9, 10: Uppercase word > 3 letters (+1)
    - line 13, 14: link_count > 0 but <= 3 (+1)
    - line 15, 16, 17, 18: sender_known True and negative score reset to 0
    """
    score = score_message("HELLO", True, 1)
    # uppercase HELLO: +1, link: +1 -> total 2. sender_known: 2 - 3 = -1 -> clamped to 0
    assert score == 0


def test_classify_all_levels():
    """
    Covers lines in classify:
    - line 23, 24: score >= 8 -> 'spam'
    - line 25, 26: score >= 4 -> 'suspicious'
    - line 27: score < 4 -> 'clean'
    """
    assert classify(9) == "spam"
    assert classify(5) == "suspicious"
    assert classify(1) == "clean"


def test_filter_inbox():
    """
    Covers lines in filter_inbox:
    - line 31: counts initialization
    - line 32, 33, 34: message iteration, classification, and counter increment
    - line 35: return counts
    """
    msgs = [
        ("free urgent prize", False, 4),
        ("hello friend", False, 0)
    ]
    counts = filter_inbox(msgs)
    assert counts["spam"] == 1
    assert counts["clean"] == 1
    assert counts["suspicious"] == 0


def test_inbox_status_all_outcomes():
    """
    Covers lines in inbox_status:
    - line 39, 40, 41: total == 0 -> 'empty'
    - line 42, 43, 44: ratio > 0.5 -> 'flooded'
    - line 45, 46: ratio > 0.2 -> 'noisy'
    - line 47: fallback -> 'healthy'
    """
    assert inbox_status({"spam": 0, "suspicious": 0, "clean": 0}) == "empty"
    assert inbox_status({"spam": 3, "suspicious": 0, "clean": 1}) == "flooded"
    assert inbox_status({"spam": 1, "suspicious": 0, "clean": 2}) == "noisy"
    assert inbox_status({"spam": 0, "suspicious": 1, "clean": 3}) == "healthy"
