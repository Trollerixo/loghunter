# plugins/apache_parser.py
import re
from typing import List
from core.engine import LogEntry

APACHE_RE = re.compile(
    r'^(?P<ip>\S+) \S+ \S+ \[(?P<time>[^\]]+)\] '
    r'"(?P<method>\S+) (?P<path>\S+) \S+" '
    r'(?P<status>\d{3}) (?P<size>\S+)'
    r'(?: "(?P<referer>[^"]*)" "(?P<ua>[^"]*)")?'
)

def parse(lines: List[str]) -> List[LogEntry]:
    entries = []
    for line in lines:
        if not line.strip():
            continue
        m = APACHE_RE.match(line)
        if m:
            g = m.groupdict()
            entry = LogEntry(
                raw=line,
                timestamp=g.get("time"),
                source=g.get("ip"),
                message=f'{g["method"]} {g["path"]} -> {g["status"]}',
                fields={
                    "ip":         g.get("ip"),
                    "method":     g.get("method"),
                    "path":       g.get("path"),
                    "status":     int(g.get("status", 0)),
                    "size":       g.get("size"),
                    "referer":    g.get("referer"),
                    "user_agent": g.get("ua"),
                },
            )
        else:
            entry = LogEntry(raw=line, message=line)
        entries.append(entry)
    return entries