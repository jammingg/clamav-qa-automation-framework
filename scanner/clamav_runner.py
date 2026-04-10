import logging
import os
import subprocess
from typing import Any, Dict

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "test_run.log")

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename="logs/test_run.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

class ClamAVRunner:
    def __init__(self, service_name: str = "clamav"):
        self.service_name = service_name

    def is_service_running(self) -> bool:
        command = [
            "docker",
            "compose",
            "ps",
            "--status",
            "running",
        ]

        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        return self.service_name in completed.stdout

    def scan_file(self, container_file_path: str) -> Dict[str, Any]:
        logging.info(f"Starting scan for file: {container_file_path}")

        if not self.is_service_running():
            logging.error(f'Service "{self.service_name}" is not running')
            return {
                "file_path": container_file_path,
                "status": "environment_error",
                "infected": None,
                "signature": None,
                "return_code": None,
                "stdout": "",
                "stderr": f'Service "{self.service_name}" is not running',
            }

        command = [
            "docker",
            "compose",
            "exec",
            "-T",
            self.service_name,
            "clamscan",
            container_file_path,
        ]

        logging.info(f"Running command: {' '.join(command)}")

        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        stdout = completed.stdout.strip()
        stderr = completed.stderr.strip()
        return_code = completed.returncode

        logging.info(f"Return code: {return_code}")
        logging.info(f"Stdout: {stdout}")
        logging.info(f"Stderr: {stderr}")

        infected = None
        signature = None
        status = "scan_error"

        if return_code == 0:
            infected = False
            status = "clean"

        elif return_code == 1:
            infected = True
            status = "infected"

            for line in stdout.splitlines():
                if line.endswith("FOUND"):
                    parts = line.split(": ", 1)
                    if len(parts) == 2:
                        signature = parts[1].removesuffix(" FOUND").strip()
                    break

        elif "No such file or directory" in stdout or "No such file or directory" in stderr:
            status = "file_error"

        return {
            "file_path": container_file_path,
            "status": status,
            "infected": infected,
            "signature": signature,
            "return_code": return_code,
            "stdout": stdout,
            "stderr": stderr,
        }


if __name__ == "__main__":
    runner = ClamAVRunner()
    sample_path = "/data/samples/clean/hello.txt"
    result = runner.scan_file(sample_path)

    print("Scan result:")
    for key, value in result.items():
        print(f"{key}: {value}")