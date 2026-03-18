import subprocess
from typing import Dict, Optional


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

        if not self.is_service_running():
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

        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        stdout = completed.stdout.strip()
        stderr = completed.stderr.strip()
        return_code = completed.returncode
        infected = None
        signature = None
        status = "scan_error"

        # Typical infected output:
        # /data/samples/malicious/eicar.txt: Eicar-Test-Signature FOUND
        
        # Typical clean output:
        # /data/samples/clean/hello.txt: OK

        for line in stdout.splitlines():
            if line.endswith("FOUND"):
                infected = True
                status = "infected"
                # Extract signature between ": " and " FOUND"
                parts = line.split(": ", 1)
                if len(parts) == 2:
                    right_side = parts[1]
                    signature = right_side.removesuffix(" FOUND").strip()
                break

        if return_code == 0:
            infected = False
            status = "clean"


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

    # sample_path = "/data/samples/malicious/eicar.txt"
    sample_path = "/data/samples/clean/hello.txt"
    
    result = runner.scan_file(sample_path)

    print("Scan result:")
    for key, value in result.items():
        print(f"{key}: {value}")