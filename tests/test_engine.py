# tests/test_engine.py
import pytest
from core.engine import SearchEngine, LogEntry

@pytest.fixture
def engine():
    return SearchEngine()

@pytest.fixture
def sample_entries():
    return [
        LogEntry(raw="Jan 1 00:00:01 host sshd: Failed password for root from 1.2.3.4",
                 message="Failed password for root from 1.2.3.4"),
        LogEntry(raw="Jan 1 00:00:02 host sshd: Accepted password for admin from 5.6.7.8",
                 message="Accepted password for admin from 5.6.7.8"),
        LogEntry(raw="Jan 1 00:00:03 host kernel: error reading disk sector",
                 message="error reading disk sector"),
        LogEntry(raw="Jan 1 00:00:04 host nginx: GET /admin HTTP/1.1 200",
                 message="GET /admin HTTP/1.1 200"),
    ]

def test_keyword_match(engine, sample_entries):
    results = engine.search(sample_entries, keyword="Failed password")
    assert len(results) == 1

def test_regex_match(engine, sample_entries):
    results = engine.search(sample_entries, pattern=r"password for \w+")
    assert len(results) == 2

def test_severity_detection(engine, sample_entries):
    assert engine.detect_severity(sample_entries[2]) == "error"

def test_severity_filter(engine, sample_entries):
    results = engine.search(sample_entries, severity_filter="error")
    assert all(e.level == "error" for e in results)

def test_no_filter_returns_all(engine, sample_entries):
    assert len(engine.search(sample_entries)) == len(sample_entries)

def test_case_insensitive_default(engine, sample_entries):
    assert len(engine.search(sample_entries, keyword="failed password")) == 1

def test_case_sensitive(engine, sample_entries):
    assert len(engine.search(sample_entries, keyword="failed password", case_sensitive=True)) == 0
