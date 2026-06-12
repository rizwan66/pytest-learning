import logging
import sys

logger = logging.getLogger(__name__)


class ReportPrinter:
    def __init__(self, name: str):
        self.name = name

    def print_summary(self, items: list) -> None:
        print(f"=== {self.name} Report ===")
        if not items:
            print("  (no items)")
            return
        for i, item in enumerate(items, 1):
            print(f"  {i}. {item}")
        print(f"Total: {len(items)}")

    def print_to_stderr(self, message: str) -> None:
        print(f"ERROR: {message}", file=sys.stderr)


class AuditLogger:
    def __init__(self, service_name: str):
        self.service_name = service_name
        self._log = logging.getLogger(f"audit.{service_name}")

    def log_access(self, user: str, resource: str) -> None:
        self._log.info("ACCESS user=%s resource=%s", user, resource)

    def log_denied(self, user: str, resource: str, reason: str) -> None:
        self._log.warning("DENIED user=%s resource=%s reason=%s", user, resource, reason)

    def log_error(self, message: str) -> None:
        self._log.error("ERROR service=%s msg=%s", self.service_name, message)

    def process(self, items: list) -> int:
        self._log.debug("Processing %d items", len(items))
        count = 0
        for item in items:
            if item:
                self._log.info("Processed item: %s", item)
                count += 1
            else:
                self._log.warning("Skipped empty item")
        self._log.info("Done. Processed %d/%d items", count, len(items))
        return count
