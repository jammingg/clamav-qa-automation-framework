from scanner.clamav_runner import ClamAVRunner


runner = ClamAVRunner()


def fake_is_service_running():
    return False


def test_environment_check_prevents_scan_when_service_is_down(monkeypatch):
    monkeypatch.setattr(runner, "is_service_running", fake_is_service_running)

    result = runner.scan_file("/data/samples/malicious/eicar.txt")

    assert result["status"] == "environment_error"
    assert result["infected"] is None
    assert result["return_code"] is None
