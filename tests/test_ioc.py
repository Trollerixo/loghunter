# tests/test_ioc.py
import pytest
from core.ioc import IOCMatcher

@pytest.fixture
def ioc_matcher(tmp_path):
    ip_file   = tmp_path / "ips.txt"
    ua_file   = tmp_path / "uas.txt"
    hash_file = tmp_path / "hashes.txt"
    ip_file.write_text("185.220.101.1\n45.33.32.156\n")
    ua_file.write_text("masscan\nnmap scripting engine\n")
    hash_file.write_text("e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855\n")
    return IOCMatcher(str(ip_file), str(ua_file), str(hash_file))

def test_ip_hit(ioc_matcher):
    hits = ioc_matcher.scan("Connection from 185.220.101.1 port 4444")
    assert any("MALICIOUS_IP" in h for h in hits)

def test_ua_hit(ioc_matcher):
    hits = ioc_matcher.scan('User-Agent: masscan/1.0')
    assert any("BAD_UA" in h for h in hits)

def test_hash_hit(ioc_matcher):
    hits = ioc_matcher.scan("file hash: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
    assert any("MALWARE_HASH" in h for h in hits)

def test_no_hit(ioc_matcher):
    assert ioc_matcher.scan("normal log line") == []