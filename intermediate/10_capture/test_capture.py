# INTERMEDIATE LEVEL — LESSON 10: Capturing Output
#
# KEY CONCEPTS:
#   - capsys: capture sys.stdout / sys.stderr (works for print())
#   - capfd: capture file descriptor 1/2 (works for C extensions too)
#   - caplog: capture logging output with level, logger, and message assertions
#   - capsys.readouterr() returns a named tuple (out, err) — call it once per check
#
# RUN: pytest intermediate/10_capture/ -v -s
#      (note: -s disables capture for normal output; remove it to see capsys work)

import logging
import pytest
from reporter import ReportPrinter, AuditLogger


# ==========================================================
# PART 1: capsys — capturing print() / sys.stdout / sys.stderr
# ==========================================================

@pytest.fixture
def printer():
    return ReportPrinter("Test")


def test_print_summary_outputs_header(printer, capsys):
    printer.print_summary(["apple", "banana"])
    captured = capsys.readouterr()
    assert "Test Report" in captured.out


def test_print_summary_lists_items(printer, capsys):
    printer.print_summary(["x", "y", "z"])
    captured = capsys.readouterr()
    assert "1. x" in captured.out
    assert "2. y" in captured.out
    assert "3. z" in captured.out


def test_print_summary_shows_total(printer, capsys):
    printer.print_summary(["a", "b"])
    out, _ = capsys.readouterr()
    assert "Total: 2" in out


def test_print_summary_empty_list(printer, capsys):
    printer.print_summary([])
    out, _ = capsys.readouterr()
    assert "(no items)" in out
    assert "Total" not in out


def test_stderr_output(printer, capsys):
    printer.print_to_stderr("disk full")
    _, err = capsys.readouterr()
    assert "ERROR: disk full" in err
    # stdout should be clean
    out, _ = capsys.readouterr()
    assert out == ""


def test_no_unexpected_stdout(printer, capsys):
    # Verify a function produces NO output
    result = printer.print_summary.__doc__  # attribute access, no side-effects
    out, err = capsys.readouterr()
    assert out == ""
    assert err == ""


# --- readouterr() resets the buffer each call ---

def test_capsys_resets_between_readouterr_calls(printer, capsys):
    printer.print_summary(["first"])
    out1, _ = capsys.readouterr()
    printer.print_summary(["second"])
    out2, _ = capsys.readouterr()
    # Each call only has the lines printed since the last readouterr
    assert "first" not in out2
    assert "second" in out2


# --- capsys.disabled(): temporarily stop capture so print IS visible ---

def test_with_capture_disabled(capsys):
    with capsys.disabled():
        # This prints directly to the terminal (visible when running pytest -s)
        print("This goes to the real stdout, bypassing capture")
    # After the context manager, capture resumes
    _, _ = capsys.readouterr()


# ==========================================================
# PART 2: caplog — capturing logging records
# ==========================================================

@pytest.fixture
def auditor():
    return AuditLogger("payments")


def test_access_log_is_emitted(auditor, caplog):
    with caplog.at_level(logging.INFO, logger="audit.payments"):
        auditor.log_access("alice", "/admin")
    assert "ACCESS" in caplog.text
    assert "alice" in caplog.text


def test_denied_log_level_is_warning(auditor, caplog):
    with caplog.at_level(logging.WARNING, logger="audit.payments"):
        auditor.log_denied("bob", "/secret", "insufficient permissions")
    record = caplog.records[0]
    assert record.levelno == logging.WARNING
    assert "DENIED" in record.message


def test_error_log_is_captured(auditor, caplog):
    with caplog.at_level(logging.ERROR, logger="audit.payments"):
        auditor.log_error("connection timeout")
    assert any("connection timeout" in r.message for r in caplog.records)


def test_no_logs_on_empty_input(auditor, caplog):
    with caplog.at_level(logging.DEBUG, logger="audit.payments"):
        count = auditor.process([])
    assert count == 0
    # Only DEBUG and INFO logs — no warnings or errors
    error_records = [r for r in caplog.records if r.levelno >= logging.WARNING]
    assert len(error_records) == 0


def test_process_warns_on_empty_items(auditor, caplog):
    with caplog.at_level(logging.DEBUG, logger="audit.payments"):
        auditor.process(["valid", "", "also valid"])
    warnings = [r for r in caplog.records if r.levelno == logging.WARNING]
    assert len(warnings) == 1
    assert "Skipped" in warnings[0].message


def test_process_count(auditor, caplog):
    with caplog.at_level(logging.INFO, logger="audit.payments"):
        count = auditor.process(["a", "b", "c"])
    assert count == 3
    # The final "Done" log should mention count
    done_records = [r for r in caplog.records if "Done" in r.message]
    assert len(done_records) == 1
    assert "3/3" in done_records[0].message


def test_caplog_logger_filter(auditor, caplog):
    # Only capture logs from the specific logger — ignore root logger noise
    with caplog.at_level(logging.INFO, logger="audit.payments"):
        auditor.log_access("carol", "/reports")
    for record in caplog.records:
        assert record.name.startswith("audit.payments")


# EXERCISE:
# 1. Write a test that verifies log_access emits at INFO level (not DEBUG or WARNING).
# 2. Add a `print_to_stderr` call inside `process()` on error, then test for it
#    using both caplog AND capsys in the same test.
# 3. Use caplog.set_level(logging.DEBUG) (without context manager) and verify
#    debug messages appear — what's the difference from at_level()?
