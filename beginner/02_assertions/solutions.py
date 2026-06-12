# SOLUTIONS — Lesson 02: Rich Assertions

from string_utils import reverse, word_count, extract_emails
import pytest


def test_reverse_pytest():
    assert reverse("pytest") == "tsetyp"


def test_word_count_with_extra_spaces():
    # str.split() without args handles multiple spaces correctly
    assert word_count("  hello  ") == 1


def test_extract_emails_no_valid_emails():
    emails = extract_emails("no at signs here, just plain text and numbers 123")
    assert emails == []
