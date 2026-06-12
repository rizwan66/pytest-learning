# INTERMEDIATE LEVEL — LESSON 11: Time Mocking with freezegun
#
# KEY CONCEPTS:
#   - Production code that calls date.today() / datetime.now() is hard to test
#     without freezegun — the result changes every second
#   - @freeze_time("YYYY-MM-DD") freezes all time calls inside the test
#   - freeze_time patches: datetime.now(), date.today(), time.time(), etc.
#   - You can move time forward inside a test using freezer.move_to()
#   - Works as decorator, context manager, or class decorator
#
# SETUP: pip install freezegun
# RUN:   pytest intermediate/11_freezegun/ -v

from datetime import date, timedelta
import pytest
from freezegun import freeze_time
from subscription import Subscription, TrialReminder


# ==========================================================
# PART 1: @freeze_time as a decorator
# ==========================================================

@freeze_time("2026-01-01")
def test_subscription_starts_on_frozen_date():
    sub = Subscription(user_id="u1", plan="free")
    assert sub.start_date == date(2026, 1, 1)


@freeze_time("2026-01-01")
def test_trial_end_is_14_days_later():
    sub = Subscription(user_id="u1", plan="free")
    assert sub.trial_end == date(2026, 1, 15)


@freeze_time("2026-01-07")  # day 7 of a trial that started Jan 1
def test_still_in_trial_during_trial_period():
    sub = Subscription(user_id="u1", plan="free", start_date=date(2026, 1, 1))
    assert sub.is_in_trial() is True


@freeze_time("2026-01-15")  # last day (day 14)
def test_still_in_trial_on_last_day():
    sub = Subscription(user_id="u1", plan="free", start_date=date(2026, 1, 1))
    assert sub.is_in_trial() is True


@freeze_time("2026-01-16")  # day after trial ends
def test_trial_expired_after_14_days():
    sub = Subscription(user_id="u1", plan="free", start_date=date(2026, 1, 1))
    assert sub.is_in_trial() is False
    assert sub.is_expired() is True


@freeze_time("2026-01-08")  # 7 days left in trial
def test_days_remaining_in_trial():
    sub = Subscription(user_id="u1", plan="free", start_date=date(2026, 1, 1))
    assert sub.days_remaining_in_trial() == 7


@freeze_time("2026-01-16")  # trial over
def test_days_remaining_is_zero_after_expiry():
    sub = Subscription(user_id="u1", plan="free", start_date=date(2026, 1, 1))
    assert sub.days_remaining_in_trial() == 0


# ==========================================================
# PART 2: freeze_time as a context manager (within a test)
# ==========================================================

def test_is_in_trial_transitions_correctly():
    sub = Subscription(user_id="u2", plan="free", start_date=date(2026, 3, 1))

    with freeze_time("2026-03-10"):       # day 10 — still in trial
        assert sub.is_in_trial() is True

    with freeze_time("2026-03-15"):       # day 15 — last day
        assert sub.is_in_trial() is True

    with freeze_time("2026-03-16"):       # day 15 + 1 — expired
        assert sub.is_in_trial() is False


# ==========================================================
# PART 3: Moving time with freezer.move_to()
# ==========================================================

def test_reminder_sent_at_7_days_remaining():
    sub = Subscription(user_id="u3", plan="free", start_date=date(2026, 6, 1))
    reminder = TrialReminder(sub)

    # Trial started June 1, ends June 15. 7 days left = June 8.
    with freeze_time("2026-06-08") as freezer:
        msg = reminder.check_and_remind()
        assert msg is not None
        assert "7 days" in msg

        # Move to the last day
        freezer.move_to("2026-06-14")
        msg = reminder.check_and_remind()
        assert msg is not None
        assert "Last day" in msg


def test_reminder_on_expiry_day():
    sub = Subscription(user_id="u4", plan="free", start_date=date(2026, 5, 1))
    reminder = TrialReminder(sub)

    with freeze_time("2026-05-16"):  # day after trial ends (May 1 + 14 = May 15, expired May 16)
        msg = reminder.check_and_remind()
        assert msg is not None
        assert "expired" in msg.lower()


# ==========================================================
# PART 4: Parametrizing frozen dates
# ==========================================================

@pytest.mark.parametrize("frozen_date, expected_in_trial", [
    ("2026-02-01", True),   # day 0: start date
    ("2026-02-07", True),   # day 6: mid-trial
    ("2026-02-15", True),   # day 14: Feb 1 + 14 = Feb 15 (trial_end) — still in trial
    ("2026-02-16", False),  # day 15: first day after trial_end
    ("2026-03-01", False),  # long after
])
def test_trial_status_at_various_dates(frozen_date, expected_in_trial):
    with freeze_time(frozen_date):
        sub = Subscription(user_id="test", plan="free", start_date=date(2026, 2, 1))
        assert sub.is_in_trial() == expected_in_trial


# ==========================================================
# PART 5: @freeze_time on a class
# ==========================================================

@freeze_time("2026-04-01")
class TestSubscriptionInApril:
    """All tests in this class run with time frozen at 2026-04-01."""

    def test_today_is_april_1(self):
        assert date.today() == date(2026, 4, 1)

    def test_pro_plan_not_expired(self):
        sub = Subscription(user_id="pro_user", plan="pro", start_date=date(2026, 3, 18))
        assert not sub.is_expired()  # pro plans don't expire even after trial

    def test_free_plan_expired_after_trial(self):
        sub = Subscription(user_id="free_user", plan="free", start_date=date(2026, 3, 1))
        # March 1 + 14 days = March 15 trial end; April 1 is after
        assert sub.is_expired() is True


# EXERCISE:
# 1. Write a test that freezes time on New Year's Eve and checks that a trial
#    starting that day ends on January 14th of the next year.
# 2. Use move_to() to simulate a user who upgrades from "free" to "pro" on day 10
#    of their trial — verify is_expired() is False on day 20.
# 3. Parametrize test_trial_status_at_various_dates with 3 more edge-case dates.
