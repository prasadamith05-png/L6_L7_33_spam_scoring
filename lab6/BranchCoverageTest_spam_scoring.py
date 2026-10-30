import pytest
from spam_scoring import score_message, classify, filter_inbox, inbox_status

# ==============================================================================
# Branch Coverage Test Suite (Decision & Branch Coverage Analysis)
# Focus: Ensure every decision branch (if/elif/else/loops, true and false branches,
# boundary values, and compound conditions) in spam_scoring.py evaluates to BOTH
# True and False, achieving 100% Branch Coverage.
# ==============================================================================

class TestScoreMessageBranchCoverage:
    """Tests covering all branches of score_message."""

    def test_empty_message_zero_links_unknown_sender(self):
        # Loop branch: 0 iterations of for-loop (text.split() is empty)
        # Link branch: link_count <= 0
        # Sender branch: sender_known is False
        assert score_message("", False, 0) == 0

    def test_spam_words_with_punctuation(self):
        # Spam word branch: True branch for word in SPAM_WORDS (tested with punctuation strip)
        # Link branch: link_count > 3 (+4)
        assert score_message("winner! urgent. prize, cash free", False, 5) == (5 * 2) + 4

    def test_word_uppercase_and_length_gt_3(self):
        # Compound elif branch: word.isupper() == True AND len(word) > 3 == True
        assert score_message("NOTICE", False, 0) == 1

    def test_word_uppercase_but_length_le_3(self):
        # Compound elif branch: word.isupper() == True BUT len(word) > 3 == False
        # Evaluates first part True, second part False
        assert score_message("NOW", False, 0) == 0

    def test_word_lowercase_not_in_spam_words(self):
        # Spam word False branch, and elif word.isupper() False branch
        assert score_message("regular update meeting", False, 0) == 0

    def test_link_count_between_1_and_3(self):
        # Link branches: link_count > 3 is False, but link_count > 0 is True (+1)
        assert score_message("hello", False, 2) == 1

    def test_sender_known_with_score_exceeding_3(self):
        # Branch 15 (sender_known True) -> score -= 3
        # Branch 17 -> 19 (score < 0 is FALSE, so score is NOT reset to 0)
        # 3 spam words = 6 points; 6 - 3 = 3 (> 0)
        assert score_message("free prize cash", True, 0) == 3

    def test_sender_known_with_score_below_3_clamped_to_zero(self):
        # Branch 15 (sender_known True) -> score -= 3
        # Branch 17 -> 18 (score < 0 is TRUE, clamped to 0)
        # 1 point (short link); 1 - 3 = -2 -> clamped to 0
        assert score_message("hello", True, 1) == 0

    def test_sender_known_with_exact_zero_score(self):
        # sender_known True on 0 points: 0 - 3 = -3 -> clamped to 0
        assert score_message("hello", True, 0) == 0


class TestClassifyBranchCoverage:
    """Tests covering all branches and boundaries of classify."""

    def test_classify_spam_at_and_above_boundary(self):
        # score >= 8: True branch
        assert classify(8) == "spam"
        assert classify(12) == "spam"

    def test_classify_suspicious_at_and_above_boundary(self):
        # score >= 8 is False; score >= 4 is True
        assert classify(4) == "suspicious"
        assert classify(7) == "suspicious"

    def test_classify_clean_below_suspicious(self):
        # score >= 8 is False; score >= 4 is False -> "clean"
        assert classify(3) == "clean"
        assert classify(0) == "clean"
        assert classify(-1) == "clean"


class TestFilterInboxBranchCoverage:
    """Tests covering filter_inbox branches."""

    def test_filter_empty_inbox(self):
        # Loop branch: 0 iterations
        counts = filter_inbox([])
        assert counts == {"spam": 0, "suspicious": 0, "clean": 0}

    def test_filter_inbox_with_mixed_messages(self):
        # Loop branch: >= 1 iterations covering spam, suspicious, and clean
        messages = [
            ("free prize cash winner urgent", False, 5),   # spam: 5*2 + 4 = 14 (>=8)
            ("free cash", False, 1),                        # suspicious: 2*2 + 1 = 5 (>=4)
            ("meeting at noon tomorrow", False, 0)          # clean: 0 (<4)
        ]
        counts = filter_inbox(messages)
        assert counts == {"spam": 1, "suspicious": 1, "clean": 1}


class TestInboxStatusBranchCoverage:
    """Tests covering all branches, thresholds, and boundaries of inbox_status."""

    def test_inbox_empty_branch(self):
        # total == 0: True branch
        assert inbox_status({"spam": 0, "suspicious": 0, "clean": 0}) == "empty"

    def test_inbox_flooded_branch(self):
        # ratio > 0.5: True branch (e.g. 2 / 3 = 0.666 > 0.5)
        assert inbox_status({"spam": 2, "suspicious": 0, "clean": 1}) == "flooded"

    def test_inbox_boundary_ratio_exactly_half(self):
        # Boundary: ratio == 0.5 (1 / 2 = 0.5)
        # ratio > 0.5 is False, but ratio > 0.2 is True -> "noisy"
        assert inbox_status({"spam": 1, "suspicious": 0, "clean": 1}) == "noisy"

    def test_inbox_noisy_branch(self):
        # ratio > 0.2: True branch (e.g. 1 / 4 = 0.25 > 0.2)
        assert inbox_status({"spam": 1, "suspicious": 1, "clean": 2}) == "noisy"

    def test_inbox_boundary_ratio_exactly_twenty_percent(self):
        # Boundary: ratio == 0.2 (1 / 5 = 0.2)
        # ratio > 0.5 is False, ratio > 0.2 is False -> "healthy"
        assert inbox_status({"spam": 1, "suspicious": 2, "clean": 2}) == "healthy"

    def test_inbox_healthy_zero_spam(self):
        # ratio == 0.0 <= 0.2 -> "healthy"
        assert inbox_status({"spam": 0, "suspicious": 3, "clean": 2}) == "healthy"
