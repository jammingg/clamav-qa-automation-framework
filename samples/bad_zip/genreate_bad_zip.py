import zipfile
from pathlib import Path

samples_dir = Path("samples/bad_zip")
samples_dir.mkdir(parents=True, exist_ok=True)

zip_path = samples_dir / "bad.zip"

with zipfile.ZipFile(zip_path, "w") as zf:
    zf.writestr("hello.txt", "hello world")

with open(zip_path, "r+b") as f:
    f.seek(-10, 2)
    f.write(b"XXXXXXXXXX")

print(f"Created corrupted zip: {zip_path}")