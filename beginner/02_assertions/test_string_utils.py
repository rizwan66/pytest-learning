# BEGINNER LEVEL — LESSON 2: Rich Assertions
#
# KEY CONCEPTS:
#   - pytest shows the full diff on assertion failure — no assertEqual needed
#   - assert with collections: `in`, `not in`, len(), startswith(), etc.
#   - approx() for floating-point comparisons
#
# RUN: pytest beginner/02_assertions/ -v

import pytest
from string_utils import reverse, is_palindrome, word_count, capitalize_words, truncate, extract_emails


# --- String equality ---

def test_reverse_simple():
    assert reverse("hello") == "olleh"


def test_reverse_empty_string():
    assert reverse("") == ""


def test_reverse_single_char():
    assert reverse("a") == "a"


# --- Boolean / truthiness ---

def test_palindrome_simple_word():
    assert is_palindrome("racecar")


def test_palindrome_with_spaces():
    assert is_palindrome("a man a plan a canal panama")


def test_not_palindrome():
    assert not is_palindrome("hello")


# --- Numeric assertions ---

def test_word_count_normal():
    assert word_count("hello world foo") == 3


def test_word_count_empty_string():
    assert word_count("") == 0


def test_word_count_only_spaces():
    assert word_count("   ") == 0


# --- Substring / containment ---

def test_capitalize_contains_expected_word():
    result = capitalize_words("hello world")
    assert "Hello" in result
    assert "World" in result


def test_capitalize_full_result():
    assert capitalize_words("the quick brown fox") == "The Quick Brown Fox"


# --- Length checks ---

def test_truncate_short_string_unchanged():
    s = "hi"
    assert truncate(s, 10) == "hi"
    assert len(truncate(s, 10)) == 2


def test_truncate_long_string():
    result = truncate("hello world", 5)
    assert result == "hello..."
    assert len(result) == 8  # 5 + len("...")


def test_truncate_custom_suffix():
    result = truncate("hello world", 5, suffix="—")
    assert result.endswith("—")


# --- List assertions ---

def test_extract_emails_finds_emails():
    text = "Contact us at support@example.com or sales@company.org"
    emails = extract_emails(text)
    assert len(emails) == 2
    assert "support@example.com" in emails
    assert "sales@company.org" in emails


def test_extract_emails_empty_when_none():
    emails = extract_emails("no emails here")
    assert emails == []
    assert len(emails) == 0


# --- Floating point: use pytest.approx ---

def test_approx_basic():
    # Never do:  0.1 + 0.2 == 0.3  — it's False due to float precision!
    assert 0.1 + 0.2 == pytest.approx(0.3)


def test_approx_with_tolerance():
    assert 1.0001 == pytest.approx(1.0, rel=1e-3)


# EXERCISE:
# 1. reverse("pytest") — what do you expect? Write the test.
# 2. Test that word_count("  hello  ") returns 1 (strip handles extra spaces).
# 3. Test extract_emails on a string with NO valid emails.
