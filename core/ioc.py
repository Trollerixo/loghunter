# core/ioc.py
import re
import ipaddress
from pathlib import Path
from typing import List, Set

class IOCMatcher:
    def __init__(self, ip_blacklist_path: str, ua_blacklist_path: str, hash_blacklist_path: str):
        self.bad_ips: Set[str]    = self._load(ip_blacklist_path)
        self.bad_uas: Set[str]    = self._load(ua_blacklist_path)
        self.bad_hashes: Set[str] = self._load(hash_blacklist_path)
        self._ip_re   = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
        self._hash_re = re.compile(r'\b[a-fA-F0-9]{64}\b')  # SHA256

    def _load(self, path: str) -> Set[str]:
        p = Path(path)
        if not p.exists():
            return set()
        return {
            line.strip().lower()
            for line in p.read_text().splitlines()
            if line.strip() and not line.startswith('#')
        }

    def _check_ips(self, text: str) -> List[str]:
        hits = []
        for ip_str in self._ip_re.findall(text):
            try:
                ip = ipaddress.ip_address(ip_str)
                if not ip.is_private and ip_str in self.bad_ips:
                    hits.append(f"MALICIOUS_IP:{ip_str}")
            except ValueError:
                pass
        return hits

    def _check_hashes(self, text: str) -> List[str]:
        return [
            f"MALWARE_HASH:{h}"
            for h in self._hash_re.findall(text)
            if h.lower() in self.bad_hashes
        ]

    def _check_uas(self, text: str) -> List[str]:
        lower = text.lower()
        return [f"BAD_UA:{ua}" for ua in self.bad_uas if ua in lower]

    def scan(self, text: str) -> List[str]:
        return self._check_ips(text) + self._check_hashes(text) + self._check_uas(text)