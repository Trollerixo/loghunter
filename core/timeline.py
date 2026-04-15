# core/timeline.py
import re
from typing import List
from core.engine import LogEntry

TS_PATTERNS = [
    re.compile(r'(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2})'),
    re.compile(r'(\w{3}\s+\d+\s+\d{2}:\d{2}:\d{2})'),
    re.compile(r'(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2})'),
]

def extract_sortable_ts(entry: LogEntry) -> str:
    for pattern in TS_PATTERNS:
        m = pattern.search(entry.raw)
        if m:
            return m.group(1)
    return entry.timestamp or ""

def build_timeline(entries: List[LogEntry]) -> List[LogEntry]:
    for e in entries:
        if not e.timestamp:
            e.timestamp = extract_sortable_ts(e)
    return sorted(entries, key=lambda e: e.timestamp or "")