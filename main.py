#!/usr/bin/env python3
# main.py — LogHunter entry point
import sys
import argparse
from core.parser import LogParser
from core.engine import SearchEngine
from core.ioc import IOCMatcher
from core.timeline import build_timeline
from output.terminal import TerminalOutput
from output.exporter import export_results

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="loghunter",
        description="LogHunter — Advanced Log Search & Analysis Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("files", nargs="+", help="Log file(s) to analyze")
    p.add_argument("-k", "--keyword",  help="Keyword to search for")
    p.add_argument("-r", "--regex",    help="Regex pattern to match")
    p.add_argument("-s", "--severity", choices=["critical","error","warning","info"], help="Filter by severity level")
    p.add_argument("--ioc",            action="store_true", help="Show only IOC-matched entries")
    p.add_argument("--timeline",       action="store_true", help="Reconstruct timeline across all files")
    p.add_argument("--case-sensitive", action="store_true", help="Case-sensitive keyword search")
    p.add_argument("--export",         choices=["json","csv","html"], help="Export results to file")
    p.add_argument("--output",         default="loghunter_results", help="Output filename (no extension)")
    p.add_argument("--ip-blacklist",   default="data/ip_blacklist.txt")
    p.add_argument("--ua-blacklist",   default="data/bad_useragents.txt")
    p.add_argument("--hash-blacklist", default="data/hashes.txt")
    p.add_argument("--no-color",       action="store_true", help="Disable colored output")
    return p

def main():
    args = build_parser().parse_args()

    ioc    = IOCMatcher(args.ip_blacklist, args.ua_blacklist, args.hash_blacklist)
    parser = LogParser()
    engine = SearchEngine(ioc_matcher=ioc)
    out    = TerminalOutput(color=not args.no_color)

    all_entries = []
    for filepath in args.files:
        try:
            entries = parser.parse_file(filepath)
            out.print_info(f"Parsed {len(entries)} entries from {filepath}")
            all_entries.extend(entries)
        except FileNotFoundError as e:
            out.print_error(str(e))
            sys.exit(1)

    if args.timeline:
        all_entries = build_timeline(all_entries)

    results = engine.search(
        all_entries,
        keyword=args.keyword,
        pattern=args.regex,
        severity_filter=args.severity,
        ioc_only=args.ioc,
        case_sensitive=args.case_sensitive,
    )

    out.print_results(results)
    out.print_summary(results)

    if args.export:
        export_results(results, fmt=args.export, filename=args.output)
        out.print_info(f"Results exported to {args.output}.{args.export}")

if __name__ == "__main__":
    main()