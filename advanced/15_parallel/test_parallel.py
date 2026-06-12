# ADVANCED LEVEL — LESSON 15: Parallel Testing with pytest-xdist
#
# KEY CONCEPTS:
#   - pytest-xdist runs tests in parallel across multiple worker processes
#   - -n auto: uses all available CPU cores
#   - -n 4: uses exactly 4 workers
#   - Each worker runs in its own process — NO shared memory
#   - worker_id fixture: identifies which worker is running ("gw0", "gw1", etc.)
#   - tmp_path is worker-safe (each worker gets its own temp dir)
#   - session-scoped fixtures run ONCE PER WORKER — not once total
#
# SETUP: pip install pytest-xdist
#
# RUN SERIAL:   pytest advanced/15_parallel/ -v
# RUN PARALLEL: pytest advanced/15_parallel/ -v -n auto
# RUN 2 WORKERS: pytest advanced/15_parallel/ -v -n 2
# COMPARE SPEED: pytest advanced/15_parallel/ --durations=10
#                pytest advanced/15_parallel/ --durations=10 -n auto

import time
import json
import pytest
from tasks import compute_hash, process_batch, slow_io_task, write_report, read_report, count_words


# ==========================================================
# PART 1: Tests that are naturally safe for parallel execution
#         (pure functions, no shared state)
# ==========================================================

@pytest.mark.parametrize("data,expected_prefix", [
    ("hello",    "2cf2"),
    ("world",    "486e"),
    ("pytest",   "2b01"),
    ("xdist",    "514b"),
    ("parallel", "83a0"),
    ("testing",  "cf80"),
])
def test_hash_prefix(data, expected_prefix):
    result = compute_hash(data)
    assert result.startswith(expected_prefix)


@pytest.mark.parametrize("items", [
    ["alpha", "beta", "gamma"],
    ["one", "two", "three", "four"],
    ["x"],
    ["a" * 100, "b" * 50],
])
def test_process_batch_length(items):
    results = process_batch(items)
    assert len(results) == len(items)


def test_process_batch_contains_hash():
    results = process_batch(["test"])
    assert "hash" in results[0]
    assert len(results[0]["hash"]) == 64  # sha256 hex digest


def test_process_batch_uppercases():
    results = process_batch(["hello", "world"])
    assert results[0]["upper"] == "HELLO"
    assert results[1]["upper"] == "WORLD"


# ==========================================================
# PART 2: I/O-bound tests — where parallel execution shines
#         Run serial vs. parallel to observe the speedup
# ==========================================================

@pytest.mark.parametrize("name", ["task_a", "task_b", "task_c", "task_d", "task_e"])
def test_slow_io_task(name):
    # Each test sleeps 50ms — 5 tests = 250ms serial, ~50ms parallel
    result = slow_io_task(name, delay=0.05)
    assert result == f"done:{name}"


# ==========================================================
# PART 3: File I/O — tmp_path is safe across workers
#         Each worker's tests get their own isolated temp directory
# ==========================================================

def test_write_and_read_report(tmp_path):
    data = {"status": "ok", "count": 42}
    report_path = tmp_path / "report.json"
    write_report(report_path, data)
    loaded = read_report(report_path)
    assert loaded == data


def test_multiple_reports_do_not_collide(tmp_path):
    # Each parallel worker has its own tmp_path — no collision possible
    for i in range(3):
        p = tmp_path / f"report_{i}.json"
        write_report(p, {"index": i})
    files = list(tmp_path.glob("*.json"))
    assert len(files) == 3


# ==========================================================
# PART 4: worker_id fixture — xdist-aware test logic
# ==========================================================

def test_worker_id_is_available(worker_id):
    # worker_id is "master" in serial mode, "gw0"/"gw1"/... in parallel
    assert isinstance(worker_id, str)
    assert len(worker_id) > 0


def test_worker_id_format(worker_id):
    # In parallel mode: "gw0", "gw1", etc. In serial: "master"
    assert worker_id == "master" or worker_id.startswith("gw")


def test_write_worker_specific_file(tmp_path, worker_id):
    # Use worker_id to create worker-unique filenames when needed
    path = tmp_path / f"output_{worker_id}.txt"
    path.write_text(f"from worker {worker_id}")
    assert path.read_text() == f"from worker {worker_id}"


# ==========================================================
# PART 5: Word count — CPU-bound, benefits from parallelism
# ==========================================================

@pytest.mark.parametrize("text,word,expected_count", [
    ("the cat sat on the mat", "the", 2),
    ("one two three one", "one", 2),
    ("hello world", "hello", 1),
    ("a a a a a", "a", 5),
    ("pytest is great, pytest rocks", "pytest", 2),
])
def test_word_count(text, word, expected_count):
    counts = count_words(text)
    assert counts.get(word, 0) == expected_count


def test_word_count_strips_punctuation():
    counts = count_words("hello, world! hello.")
    assert counts["hello"] == 2
    assert counts["world"] == 1


# ==========================================================
# PART 6: What NOT to do in parallel tests
# ==========================================================

# BAD PATTERN (do NOT do this) — shared mutable module-level state breaks xdist:
#
# _shared_results = []
#
# def test_appends_result():
#     _shared_results.append(1)   # another worker can't see this!
#
# def test_checks_shared_result():
#     assert len(_shared_results) == 1   # FAILS — different process
#
# SOLUTION: use tmp_path, databases, or message queues for inter-test communication.

def test_pure_functions_are_xdist_safe():
    # Pure functions with no side effects are always safe for parallel execution
    assert compute_hash("a") == compute_hash("a")
    assert process_batch(["x"]) == process_batch(["x"])


# EXERCISE:
# 1. Run `time pytest advanced/15_parallel/ -v` and then
#    `time pytest advanced/15_parallel/ -v -n auto` — compare wall-clock time.
# 2. Add --dist=loadscope to group parametrized tests together. How does it affect order?
# 3. Write a session-scoped fixture and add a print() to it — run with -n 2 -s
#    to observe it runs TWICE (once per worker).
