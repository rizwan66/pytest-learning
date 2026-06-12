from datetime import date, timedelta
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Subscription:
    user_id: str
    plan: str                          # "free" | "pro" | "enterprise"
    start_date: date = field(default_factory=date.today)
    trial_days: int = 14

    @property
    def trial_end(self) -> date:
        return self.start_date + timedelta(days=self.trial_days)

    def is_in_trial(self) -> bool:
        return date.today() <= self.trial_end

    def days_remaining_in_trial(self) -> int:
        delta = self.trial_end - date.today()
        return max(0, delta.days)

    def is_expired(self) -> bool:
        return not self.is_in_trial() and self.plan == "free"

    def upgrade(self, new_plan: str) -> None:
        if new_plan not in ("pro", "enterprise"):
            raise ValueError(f"Unknown plan: {new_plan!r}")
        self.plan = new_plan

    def renewal_date(self) -> Optional[date]:
        if self.plan == "free":
            return None
        # Paid plans renew monthly from start_date
        today = date.today()
        months_elapsed = (today.year - self.start_date.year) * 12 + (
            today.month - self.start_date.month
        )
        return date(
            self.start_date.year + (self.start_date.month + months_elapsed - 1) // 12,
            (self.start_date.month + months_elapsed - 1) % 12 + 1,
            self.start_date.day,
        )


class TrialReminder:
    def __init__(self, subscription: Subscription):
        self.sub = subscription
        self.reminders_sent: list[str] = []

    def check_and_remind(self) -> Optional[str]:
        days = self.sub.days_remaining_in_trial()
        if days == 7:
            msg = f"Trial ends in 7 days for {self.sub.user_id}"
            self.reminders_sent.append(msg)
            return msg
        if days == 1:
            msg = f"Last day of trial for {self.sub.user_id}!"
            self.reminders_sent.append(msg)
            return msg
        if days == 0 and self.sub.is_expired():
            msg = f"Trial expired for {self.sub.user_id}"
            self.reminders_sent.append(msg)
            return msg
        return None
