# core/engine.py
import re
from dataclasses import dataclass, field
from typing import List, Optional
from core.ioc import IOCMatcher

@dataclass
class LogEntry:
    raw: str
    timestamp: Optional[str] = None
    level: Optional[str] = None
    source: Optional[str] = None
    message: str = ""
    fields: dict = field(default_factory=dict)
    ioc_hits: List[str] = field(default_factory=list)

class SearchEngine:
    SEVERITY_KEYWORDS = {
        "critical": ["critical", "fatal", "panic", "emergency"],
        "error":    ["error", "err", "failed", "failure", "denied"],
        "warning":  ["warning", "warn", "invalid", "refused", "timeout"],
        "info":     ["info", "notice", "accepted", "started", "stopped"],
    }

    def __init__(self, ioc_matcher: Optional[IOCMatcher] = None):
        self.ioc_matcher = ioc_matcher

    def match_keyword(self, entry: LogEntry, keyword: str, case_sensitive: bool = False) -> bool:
        flags = 0 if case_sensitive else re.IGNORECASE
        return bool(re.search(re.escape(keyword), entry.raw, flags))

    def match_regex(self, entry: LogEntry, pattern: str) -> bool:
        try:
            return bool(re.search(pattern, entry.raw))
        except re.error as e:
            raise ValueError(f"Invalid regex pattern: {e}")

    def detect_severity(self, entry: LogEntry) -> str:
        lower = entry.raw.lower()
        for level, keywords in self.SEVERITY_KEYWORDS.items():
            if any(kw in lower for kw in keywords):
                return level
        return "info"

    def run_ioc_check(self, entry: LogEntry) -> List[str]:
        if not self.ioc_matcher:
            return []
        hits = self.ioc_matcher.scan(entry.raw)
        entry.ioc_hits = hits
        return hits

    def search(
        self,
        entries: List[LogEntry],
        keyword: Optional[str] = None,
        pattern: Optional[str] = None,
        severity_filter: Optional[str] = None,
        ioc_only: bool = False,
        case_sensitive: bool = False,
    ) -> List[LogEntry]:
        results = []
        for entry in entries:
            if keyword and not self.match_keyword(entry, keyword, case_sensitive):
                continue
            if pattern and not self.match_regex(entry, pattern):
                continue
            entry.level = entry.level or self.detect_severity(entry)
            if severity_filter and entry.level != severity_filter:
                continue
            self.run_ioc_check(entry)
            if ioc_only and not entry.ioc_hits:
                continue
            results.append(entry)
        return results