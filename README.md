# ClamAV QA Automation Framework

## Overview

This project is a Python-based QA automation framework designed to validate the behavior of a real-world malware detection system (ClamAV) in a controlled and reproducible environment.

The framework focuses on:

- Detection accuracy
- System stability
- Regression validation
- Debugging and failure analysis
- Automated reporting

---

## System Under Test

- **ClamAV** (open-source antivirus engine)
- Executed inside a Docker container via CLI (`clamscan`)

---

## Test Environment

The scanner runs inside Docker using:

`clamav/clamav-debian:stable`

This ensures:

- Environment isolation  
- Reproducibility  
- Consistent behavior across runs  

---

## Features to Validate

- Detect known malware signatures (EICAR test file)
- Avoid false positives on clean files
- Handle edge cases:
  - Missing files
  - Corrupted files
  - Unsupported formats
- Validate environment readiness (container availability)
- Generate structured reports and logs
- Support regression testing for previously identified issues

> **Note:**  
> Multiple edge cases (e.g., unsupported formats or missing files)
> may produce similar outcomes (e.g., `file_error`)
> These scenarios are still tested separately to ensure consistent behavior,
> validate system robustness, and support regression coverage.

---

## Test Types

- **Functional tests**  
  Validate correct detection behavior (clean vs infected)

- **Negative tests**  
  Validate error handling (missing files, environment issues)

- **Regression tests**  
  Ensure previously fixed bugs do not reappear

---

## Architecture

### Core Component

```
scanner/
└── clamav_runner.py
```

- Executes scans via Docker
- Parses results into structured output
- Handles environment checks

---

### Pytest Test Suite

```
tests/
├── test_functional.py
├── test_negative.py
└── test_regression.py
```

- Used for **validation**
- Ensures correctness via assertions

---

### QA Test Runner (Reporting Layer)

`run_tests.py`

- Executes test scenarios programmatically
- Collects structured results
- Generates reports (JSON + CSV)
- Prints summary output

This simulates a real-world QA automation workflow used in system verification,
validation, and automated test reporting pipelines.

---

## Reporting & Output

After running:

```bash
python run_tests.py
```

The framework generates:
### JSON Report:
- `reports/latest_report.json`
- Machine-readable structured results including:
    - Test name
    - Expected vs actual result
    - Pass/fail status
    - Return codes
    - Stdout/stderr

### CSV Report
- `reports/latest_report.csv`
- Human-readable summary for quick inspection and tracking
![Example of CSV Report](/assert/csv_report_example.png)

### Log File
- `logs/test_run.log`
- Detailed execution logs include:
    - Commands executed
    - Environment status
    - Stdout/stderr
    - Error details

### Example Summary Output

=== QA Test Summary ===
Total : 5
Passed: 4
Failed: 1

Failed tests:
- corrupted_files | expected=file_error actual=clean


---

## Status Definitions
| Status              | Description                   |
| ------------------- | ----------------------------- |
| `clean`             | No malware detected           |
| `infected`          | Malware signature detected    |
| `file_error`        | File missing or inaccessible  |
| `environment_error` | Scanner container not running |

---

## Folder Structure

```
clamav-qa-automation-framework/
│
├── scanner/
│   ├── clamav_runner.py
│   └── report_utils.py
│
├── tests/
│   ├── test_functional.py
│   ├── test_negative.py
│   ├── test_regression.py
│
├── samples/
│   ├── bad_zip/
│   ├── clean/
│   ├── corrupted/
│   └── malicious/
│
├── reports/
│
├── logs/
│
├── bugs/
│
├── run_tests.py
│
├── requirements.txt
│
└── README.md
```

---

## Quick Start

1. Start the scanner
```bash
docker compose up -d
```
2. Run automated QA tests (recommended)
```bash
python run_tests.py
```
3. Run pytest suite (validation)
```bash
python -m pytest -v
```
4. Manual scan (optional)
```bash
docker compose exec clamav clamscan /data/samples/malicious/eicar.txt
```
5. Stop the container
```bash
docker compose down
```

---

## Key Design Decisions

- Used subprocess + Docker CLI to control ClamAV execution
- Separated:
    - Test validation (pytest)
    - Test reporting (custom runner)
- Added environment checks to prevent misleading failures
- Designed structured outputs for reproducibility and debugging

---

### Future Improvements
- Batch/multi-file scan support
- Performance benchmarking
- CI/CD integration (GitHub Actions)
- Web-based reporting dashboard

---
