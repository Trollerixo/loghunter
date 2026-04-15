# core/parser.py
import re
from pathlib import Path
from typing import List
from core.engine import LogEntry
from plugins import syslog_parser, apache_parser, json_parser

class LogParser:
    FORMAT_SIGNATURES = {
        "syslog": re.compile(r'^\w{3}\s+\d+\s+\d{2}:\d{2}:\d{2}'),
        "apache": re.compile(r'^\d{1,3}(?:\.\d{1,3}){3} - .+ \['),
        "json":   re.compile(r'^\s*\{'),
    }

    def detect_format(self, line: str) -> str:
        for fmt, pattern in self.FORMAT_SIGNATURES.items():
            if pattern.match(line):
                return fmt
        return "raw"

    def parse_file(self, filepath: str) -> List[LogEntry]:
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"Log file not found: {filepath}")
        lines = path.read_text(errors="replace").splitlines()
        if not lines:
            return []
        fmt = self.detect_format(lines[0])
        parser_map = {
            "syslog": syslog_parser.parse,
            "apache": apache_parser.parse,
            "json":   json_parser.parse,
            "raw":    self._parse_raw,
        }
        return parser_map.get(fmt, self._parse_raw)(lines)

    def _parse_raw(self, lines: List[str]) -> List[LogEntry]:
        return [LogEntry(raw=line, message=line) for line in lines if line.strip()]