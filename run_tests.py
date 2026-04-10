import time
from scanner.clamav_runner import ClamAVRunner
from scanner.report_utils import build_report, write_json_report, write_csv_report


def run_case(runner, test_name, category, sample, expected_status):
    start = time.perf_counter()
    result = runner.scan_file(sample)
    duration = round(time.perf_counter() - start, 3)

    actual_status = result["status"]
    passed = actual_status == expected_status

    return {
        "test_name": test_name,
        "category": category,
        "sample": sample,
        "expected_status": expected_status,
        "actual_status": actual_status,
        "pass": passed,
        "infected": result.get("infected"),
        "signature": result.get("signature"),
        "return_code": result.get("return_code"),
        "stdout": result.get("stdout", ""),
        "stderr": result.get("stderr", ""),
        "duration_seconds": duration,
    }


def main():
    runner = ClamAVRunner()

    results = [
        run_case(
            runner,
            "test_detect_eicar_file",
            "functional",
            "/data/samples/malicious/eicar.txt",
            "infected"
        ),
        run_case(
            runner,
            "test_clean_text_file",
            "functional",
            "/data/samples/clean/hello.txt",
            "clean"
        ),
        run_case(
            runner,
            "test_missing_file",
            "negative",
            "/data/samples/clean/not_exist.txt",
            "file_error"
        ),
        run_case(
            runner,
            "unsupported_formats",
            "negative",
            "Unsupported-formats!",
            "file_error"
        ),
        run_case(
            runner,
            "corrupted_files",
            "negative",
            "data/samples/bad_zip/bad.zip",
            "file_error"
        ),
    ]

    report = build_report(results)

    write_json_report(report, "reports/latest_report.json")
    write_csv_report(results, "reports/latest_report.csv")

    print("\n=== QA Test Summary ===")
    print(f"Total : {report['summary']['total']}")
    print(f"Passed: {report['summary']['passed']}")
    print(f"Failed: {report['summary']['failed']}")

    if report["summary"]["failed"] > 0:
        print("\nFailed tests:")
        for r in results:
            if not r["pass"]:
                print(
                    f"- {r['test_name']} | "
                    f"expected={r['expected_status']} actual={r['actual_status']}"
                )


if __name__ == "__main__":
    main()