# output/terminal.py
from typing import List
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich import box
from core.engine import LogEntry

SEVERITY_COLORS = {
    "critical": "bold red",
    "error":    "red",
    "warning":  "yellow",
    "info":     "green",
}

class TerminalOutput:
    def __init__(self, color: bool = True):
        self.console = Console(highlight=color, markup=color)

    def print_info(self, msg: str):
        self.console.print(f"[bold cyan][*][/bold cyan] {msg}")

    def print_error(self, msg: str):
        self.console.print(f"[bold red][!][/bold red] {msg}")

    def print_results(self, entries: List[LogEntry]):
        table = Table(box=box.SIMPLE_HEAD, show_lines=False, expand=True)
        table.add_column("Timestamp", style="dim", no_wrap=True, width=22)
        table.add_column("Severity",  width=10)
        table.add_column("Source",    width=18)
        table.add_column("Message",   ratio=1)
        table.add_column("IOC Hits",  width=30)
        for e in entries:
            lvl   = e.level or "info"
            color = SEVERITY_COLORS.get(lvl, "white")
            ioc_str = ", ".join(e.ioc_hits) if e.ioc_hits else ""
            table.add_row(
                e.timestamp or "",
                Text(lvl.upper(), style=color),
                e.source or "",
                e.message[:120],
                Text(ioc_str, style="bold magenta") if ioc_str else "",
            )
        self.console.print(table)

    def print_summary(self, entries: List[LogEntry]):
        ioc_count = sum(1 for e in entries if e.ioc_hits)
        self.console.print(
            f"\n[bold]Summary:[/bold] [cyan]{len(entries)}[/cyan] matches | "
            f"[magenta]{ioc_count}[/magenta] IOC hits"
        )