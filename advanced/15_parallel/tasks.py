import time
import hashlib
import json
from pathlib import Path


def compute_hash(data: str, algorithm: str = "sha256") -> str:
    h = hashlib.new(algorithm)
    h.update(data.encode())
    return h.hexdigest()


def process_batch(items: list[str]) -> list[dict]:
    results = []
    for item in items:
        results.append({
            "item": item,
            "hash": compute_hash(item),
            "length": len(item),
            "upper": item.upper(),
        })
    return results


def slow_io_task(name: str, delay: float = 0.05) -> str:
    """Simulates an I/O-bound task (network, disk)."""
    time.sleep(delay)
    return f"done:{name}"


def write_report(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2))


def read_report(path: Path) -> dict:
    return json.loads(path.read_text())


def count_words(text: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for word in text.lower().split():
        word = word.strip(".,!?;:")
        counts[word] = counts.get(word, 0) + 1
    return counts
