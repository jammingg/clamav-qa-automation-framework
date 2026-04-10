import csv
import json
import os
from datetime import datetime

def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def write_json_report(report_data: dict, output_path: str) -> None:
    ensure_dir(os.path.dirname(output_path))
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2)

def write_csv_report(results: list[dict], output_path: str) -> None:
    ensure_dir(os.path.dirname(output_path))
    if not results:
        return

    fieldnames = [
        "test_name",
        "category",
        "sample",
        "expected_status",
        "actual_status",
        "pass",
        "infected",
        "return_code",
        "duration_seconds",
    ]

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow({key: row.get(key, "") for key in fieldnames})

def make_summary(results: list[dict]) -> dict:
    total = len(results)
    passed = sum(1 for r in results if r.get("pass"))
    failed = total - passed
    return {
        "total": total,
        "passed": passed,
        "failed": failed,
    }

def build_report(results: list[dict]) -> dict:
    return {
        "run_timestamp": datetime.now().isoformat(timespec="seconds"),
        "summary": make_summary(results),
        "results": results,
    }