# plugins/json_parser.py
import json
from typing import List
from core.engine import LogEntry

def parse(lines: List[str]) -> List[LogEntry]:
    entries = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
            entry = LogEntry(
                raw=line,
                timestamp=obj.get("timestamp") or obj.get("time") or obj.get("@timestamp"),
                level=obj.get("level") or obj.get("severity") or obj.get("log_level"),
                source=obj.get("host") or obj.get("source") or obj.get("hostname"),
                message=obj.get("message") or obj.get("msg") or str(obj),
                fields=obj,
            )
        except json.JSONDecodeError:
            entry = LogEntry(raw=line, message=line)
        entries.append(entry)
    return entries