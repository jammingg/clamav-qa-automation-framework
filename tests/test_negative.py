from scanner.clamav_runner import ClamAVRunner


runner = ClamAVRunner()


def test_missing_file():
    result = runner.scan_file("/data/samples/malicious/not_exist.txt")

    assert result["status"] == "scan_error"
    assert result["infected"] is None


def test_empty_file():
    result = runner.scan_file("/data/samples/corrupted/empty.txt")

    assert result["status"] == "clean"
    assert result["infected"] is False
    assert result["signature"] is None

def test_invalid_path():
    result = runner.scan_file("invalid_path")

    assert result["status"] == "scan_error"
    assert result["infected"] is None

