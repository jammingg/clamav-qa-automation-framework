from scanner.clamav_runner import ClamAVRunner


runner = ClamAVRunner()


def test_eicar_detection():
    result = runner.scan_file("/data/samples/malicious/eicar.txt")

    assert result["status"] == "infected"
    assert result["infected"] is True
    assert result["signature"] is not None

def test_clean_file():
    result = runner.scan_file("/data/samples/clean/hello.txt")

    assert result["status"] == "clean"
    assert result["infected"] is False
    assert result["signature"] is None
