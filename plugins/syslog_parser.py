# plugins/syslog_parser.py
import re
from typing import List
from core.engine import LogEntry

SYSLOG_RE = re.compile(
    r'^(?P<month>\w{3})\s+(?P<day>\d+)\s+(?P<time>\d{2}:\d{2}:\d{2})\s+'
    r'(?P<host>\S+)\s+(?P<process>\S+?)(?:\[(?P<pid>\d+)\])?:\s+(?P<message>.+)$'
)

def parse(lines: List[str]) -> List[LogEntry]:
    entries = []
    for line in lines:
        if not line.strip():
            continue
        m = SYSLOG_RE.match(line)
        if m:
            g = m.groupdict()
            ts = f"{g['month']} {g['day']} {g['time']}"
            entry = LogEntry(
                raw=line,
                timestamp=ts,
                source=g.get("host"),
                message=g.get("message", ""),
                fields={
                    "process": g.get("process"),
                    "pid":     g.get("pid"),
                },
            )
        else:
            entry = LogEntry(raw=line, message=line)
        entries.append(entry)
    return entries