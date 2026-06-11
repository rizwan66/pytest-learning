# ADVANCED LEVEL — LESSON 12: Property-Based Testing with Hypothesis
#
# KEY CONCEPTS:
#   - Instead of hand-picking inputs, Hypothesis generates 100s of examples
#   - You assert PROPERTIES (invariants) that must always hold
#   - Hypothesis shrinks failures to the minimal reproducing case
#   - Much better than example-based tests for algorithms and data transformations
#
# SETUP: pip install hypothesis
# RUN:   pytest advanced/12_property_based/ -v

import pytest
from hypothesis import given, assume, settings, HealthCheck
from hypothesis import strategies as st
from sorting import bubble_sort, merge_sort, encode_run_length, decode_run_length


# ============================================================
# PART 1: Example-based (manual) — for comparison
# ============================================================

def test_bubble_sort_manual():
    assert bubble_sort([3, 1, 2]) == [1, 2, 3]
    assert bubble_sort([]) == []
    assert bubble_sort([1]) == [1]


def test_merge_sort_manual():
    assert merge_sort([5, 3, 8, 1]) == [1, 3, 5, 8]


# ============================================================
# PART 2: Property-based — Hypothesis generates inputs
# ============================================================

# Property 1: Output is sorted
@given(st.lists(st.integers()))
def test_bubble_sort_output_is_sorted(lst):
    result = bubble_sort(lst)
    assert result == sorted(result)


@given(st.lists(st.integers()))
def test_merge_sort_output_is_sorted(lst):
    result = merge_sort(lst)
    assert result == sorted(result)


# Property 2: Length is preserved (no elements dropped or added)
@given(st.lists(st.integers()))
def test_bubble_sort_preserves_length(lst):
    assert len(bubble_sort(lst)) == len(lst)


# Property 3: Same elements (just reordered)
@given(st.lists(st.integers()))
def test_bubble_sort_preserves_elements(lst):
    assert sorted(bubble_sort(lst)) == sorted(lst)


# Property 4: Idempotent — sorting twice == sorting once
@given(st.lists(st.integers()))
def test_sort_idempotent(lst):
    once = bubble_sort(lst)
    twice = bubble_sort(once)
    assert once == twice


# Property 5: Consistent with Python's built-in sort
@given(st.lists(st.integers()))
def test_merge_sort_matches_builtin(lst):
    assert merge_sort(lst) == sorted(lst)


# --- More strategies ---

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False)))
def test_bubble_sort_floats(lst):
    result = bubble_sort(lst)
    assert result == sorted(result)


@given(st.lists(st.text(max_size=10), max_size=20))
def test_bubble_sort_strings(lst):
    result = bubble_sort(lst)
    assert result == sorted(result)


# --- assume(): discard inputs that violate a precondition ---

@given(st.lists(st.integers(), min_size=1))
def test_first_element_is_minimum(lst):
    assume(len(set(lst)) == len(lst))  # skip lists with duplicates
    result = bubble_sort(lst)
    assert result[0] == min(lst)


# --- Run-length encoding: encode -> decode is identity ---

@given(st.text(alphabet=st.characters(whitelist_categories=("Ll",)), min_size=0, max_size=50))
@settings(suppress_health_check=[HealthCheck.too_slow])
def test_encode_decode_roundtrip(s):
    # Property: decode(encode(s)) == s  (the roundtrip invariant)
    assert decode_run_length(encode_run_length(s)) == s


@given(st.text(alphabet="abc", min_size=1, max_size=30))
def test_encoded_length_is_even(s):
    encoded = encode_run_length(s)
    # Format is NcNcNc... — always even length
    assert len(encoded) % 2 == 0


# --- Stateful testing (advanced Hypothesis) ---
# Hypothesis can also drive a state machine — see Hypothesis docs on RuleBasedStateMachine


# EXERCISE:
# 1. Write a property test for merge_sort: first element <= last element (non-empty lists).
# 2. Test that bubble_sort([x]) == [x] for any integer x.
# 3. Write a property that shows encode is always longer than or equal to the original
#    (when all chars are unique — each char becomes "1c").
