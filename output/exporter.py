# output/exporter.py
import json
import csv
from typing import List
from core.engine import LogEntry

def _entry_to_dict(e: LogEntry) -> dict:
    return {
        "timestamp": e.timestamp,
        "level":     e.level,
        "source":    e.source,
        "message":   e.message,
        "ioc_hits":  e.ioc_hits,
        "raw":       e.raw,
    }

def export_json(entries: List[LogEntry], filename: str):
    with open(f"{filename}.json", "w") as f:
        json.dump([_entry_to_dict(e) for e in entries], f, indent=2)

def export_csv(entries: List[LogEntry], filename: str):
    with open(f"{filename}.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp","level","source","message","ioc_hits","raw"])
        writer.writeheader()
        for e in entries:
            d = _entry_to_dict(e)
            d["ioc_hits"] = "; ".join(d["ioc_hits"])
            writer.writerow(d)

def export_html(entries: List[LogEntry], filename: str):
    rows = ""
    for e in entries:
        ioc = ", ".join(e.ioc_hits) if e.ioc_hits else ""
        rows += (f"<tr><td>{e.timestamp or ''}</td><td>{e.level or ''}</td>"
                 f"<td>{e.source or ''}</td><td>{e.message}</td>"
                 f"<td style='color:red'>{ioc}</td></tr>\n")
    html = ("<!DOCTYPE html><html><head><title>LogHunter Report</title>"
            "<style>body{font-family:monospace;background:#111;color:#eee}"
            "table{width:100%;border-collapse:collapse}th,td{border:1px solid #333;"
            "padding:6px;text-align:left}th{background:#222}"
            "tr:nth-child(even){background:#1a1a1a}</style></head>"
            f"<body><h1>LogHunter Report</h1><p>{len(entries)} results</p>"
            "<table><tr><th>Timestamp</th><th>Level</th><th>Source</th>"
            f"<th>Message</th><th>IOC Hits</th></tr>{rows}</table></body></html>")
    with open(f"{filename}.html", "w") as f:
        f.write(html)

def export_results(entries: List[LogEntry], fmt: str, filename: str):
    {"json": export_json, "csv": export_csv, "html": export_html}[fmt](entries, filename)