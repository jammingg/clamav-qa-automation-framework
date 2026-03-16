import os
import subprocess
from typing import Dict, Optional


class ClamAVRunner:
    def __init__(self, service_name: str = "clamav"):
        self.service_name = service_name

    def scan_file(self, container_file_path: str) -> Dict[str, Optional[str]]:
        """
        Scan a file inside the Dockerized ClamAV container.

        Args:
            container_file_path: File path as seen inside the container,
                                 e.g. /data/samples/malicious/eicar.txt

        Returns:
            A dictionary containing:
            - file_path
            - infected (bool)
            - signature (str or None)
            - return_code (int)
            - stdout (str)
            - stderr (str)
        """
        command = [
            "docker",
            "compose",
            "exec",
            "-T",
            self.service_name,
            "clamscan",
            container_file_path,
        ]

        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        stdout = completed.stdout.strip()
        stderr = completed.stderr.strip()
        return_code = completed.returncode

        infected = False
        signature = None

        # Typical infected output:
        # /data/samples/malicious/eicar.txt: Eicar-Test-Signature FOUND
        #
        # Typical clean output:
        # /data/samples/clean/hello.txt: OK

        for line in stdout.splitlines():
            if line.endswith("FOUND"):
                infected = True

                # Extract signature between ": " and " FOUND"
                parts = line.split(": ", 1)
                if len(parts) == 2:
                    right_side = parts[1]
                    signature = right_side.removesuffix(" FOUND").strip()
                break

        return {
            "file_path": container_file_path,
            "infected": infected,
            "signature": signature,
            "return_code": return_code,
            "stdout": stdout,
            "stderr": stderr,
        }


if __name__ == "__main__":
    runner = ClamAVRunner()

    # sample_path = "/data/samples/malicious/eicar.txt"
    sample_path = "/data/samples/clean/hello.txt"
    
    result = runner.scan_file(sample_path)

    print("Scan result:")
    for key, value in result.items():
        print(f"{key}: {value}")