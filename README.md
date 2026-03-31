# ClamAV QA Automation Framework

## Goal

Build a Python-based QA automation framework to test a real open-source malware scanner for detection accuracy, stability, regression coverage, and debugging support.

## Test Environment

The malware scanner runs inside a Docker container using the official ClamAV image:

clamav/clamav-debian:stable

This ensures a reproducible testing environment and isolates the scanner from the host system.

## System Under Test

ClamAV, an open-source antivirus scanner executed through its command-line interface.

## Features to Validate

1. Detect safe antivirus test signatures such as the EICAR anti-malware test file
2. Avoid false positives on benign files
3. Handle empty, corrupted, zipped, and unsupported files safely
4. Generate logs and reproducible test reports
5. Replay regression tests for known failures

## Tech Stack

- Python 3
- pytest
- subprocess
- logging
- json / csv
- ClamAV

## Test Types

- Functional
- Negative
- Regression
- Basic performance
- Debugging/log validation

## Planned Folder Structure

clamav-qa-automation-framework/
│
├── scanner/
│   └── clamav_runner.py
│
├── tests/
│   ├── test_functional.py
│   ├── test_negative.py
│   ├── test_regression.py
│
├── samples/
│   ├── clean/
│   ├── malicious/
│   └── corrupted/
│
├── reports/
│
├── bugs/
│
├── run_tests.py
│
├── requirements.txt
│
└── README.md

## Success Criteria

- One-command test execution
- Reproducible reports
- Actionable failure logs
- Regression coverage for prior bugs

## Quick Start

- Start the scanner container:
    docker compose up -d

- Run a manual scan:
    docker compose exec clamav clamscan /data/samples/malicious/eicar.txt

- Run automated tests
    python -m pytest -v

- Close the scanner container:
    docker compose down
