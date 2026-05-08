#!/usr/bin/env python3
"""
log_parser.py — HTTP Log Status Code Analyzer
----------------------------------------------
A CLI tool to parse Apache/Nginx-style access log files, categorize
HTTP status codes, and generate a summary report.

Usage:
    python log_parser.py sample.log
    python log_parser.py sample.log --filter 5xx
    python log_parser.py sample.log --output json
    python log_parser.py sample.log --output csv --save report.csv
    python log_parser.py sample.log --top 5 --filter 4xx

Author: SDET-AI Mastery — Month 1 / Week 1 / Day 5
"""

import re
import sys
import json
import csv
import argparse
import io
from collections import defaultdict, Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

# ── Force UTF-8 output on Windows ────────────────────────
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except (AttributeError, io.UnsupportedOperation):
    pass  # Non-CPython or piped output

# Detect whether the terminal can render Unicode
def _supports_unicode() -> bool:
    try:
        "\u2550".encode(sys.stdout.encoding or "ascii")
        return True
    except (UnicodeEncodeError, LookupError):
        return False

UNICODE_OK = _supports_unicode()

# ─────────────────────────────────────────────
#  Data Structures
# ─────────────────────────────────────────────

@dataclass
class LogEntry:
    """Represents a single parsed log line."""
    ip: str
    timestamp: str
    method: str
    path: str
    protocol: str
    status_code: int
    response_size: int
    raw_line: str


@dataclass
class ParseResult:
    """Aggregated result of parsing a log file."""
    entries: list = field(default_factory=list)
    skipped_lines: int = 0
    total_lines: int = 0


# ─────────────────────────────────────────────
#  HTTP Status Code Metadata
# ─────────────────────────────────────────────

if UNICODE_OK:
    STATUS_CATEGORIES = {
        1: ("1xx Informational", "\u2139\ufe0f  ", "\033[94m"),   # Blue
        2: ("2xx Success",       "\u2705 ", "\033[92m"),   # Green
        3: ("3xx Redirection",   "\u21aa\ufe0f  ", "\033[96m"),   # Cyan
        4: ("4xx Client Error",  "\u26a0\ufe0f  ", "\033[93m"),   # Yellow
        5: ("5xx Server Error",  "\u274c ", "\033[91m"),   # Red
    }
else:
    STATUS_CATEGORIES = {
        1: ("1xx Informational", "[i] ", "\033[94m"),
        2: ("2xx Success",       "[+] ", "\033[92m"),
        3: ("3xx Redirection",   "[>] ", "\033[96m"),
        4: ("4xx Client Error",  "[!] ", "\033[93m"),
        5: ("5xx Server Error",  "[x] ", "\033[91m"),
    }

STATUS_DESCRIPTIONS = {
    100: "Continue",
    101: "Switching Protocols",
    200: "OK",
    201: "Created",
    204: "No Content",
    206: "Partial Content",
    301: "Moved Permanently",
    302: "Found",
    304: "Not Modified",
    307: "Temporary Redirect",
    308: "Permanent Redirect",
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    408: "Request Timeout",
    409: "Conflict",
    413: "Payload Too Large",
    422: "Unprocessable Entity",
    429: "Too Many Requests",
    500: "Internal Server Error",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Timeout",
}

RESET = "\033[0m"
BOLD  = "\033[1m"
DIM   = "\033[2m"


# ─────────────────────────────────────────────
#  Log Parser
# ─────────────────────────────────────────────

# Matches Apache/Nginx Combined Log Format:
# IP - user [timestamp] "METHOD /path PROTOCOL" STATUS SIZE "referer" "agent"
LOG_PATTERN = re.compile(
    r'(?P<ip>\S+)'           # IP address
    r'\s+\S+\s+'             # ident (usually -)
    r'(?P<user>\S+)\s+'      # user
    r'\[(?P<timestamp>[^\]]+)\]\s+'  # [timestamp]
    r'"(?P<method>[A-Z]+)\s+'        # "METHOD
    r'(?P<path>\S+)\s+'              # /path
    r'(?P<protocol>HTTP/[\d.]+)"\s+' # HTTP/1.1"
    r'(?P<status>\d{3})\s+'          # status code
    r'(?P<size>\d+)'                  # response size
)


def parse_log_file(filepath: Path) -> ParseResult:
    """Read and parse a log file, returning structured LogEntry objects."""
    result = ParseResult()

    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            for raw_line in f:
                result.total_lines += 1
                line = raw_line.strip()
                if not line:
                    result.skipped_lines += 1
                    continue

                match = LOG_PATTERN.match(line)
                if not match:
                    result.skipped_lines += 1
                    continue

                entry = LogEntry(
                    ip=match.group("ip"),
                    timestamp=match.group("timestamp"),
                    method=match.group("method"),
                    path=match.group("path"),
                    protocol=match.group("protocol"),
                    status_code=int(match.group("status")),
                    response_size=int(match.group("size")),
                    raw_line=line,
                )
                result.entries.append(entry)

    except FileNotFoundError:
        print(f"\n{BOLD}\033[91m[ERROR]{RESET} File not found: {filepath}")
        sys.exit(1)
    except PermissionError:
        print(f"\n{BOLD}\033[91m[ERROR]{RESET} Permission denied: {filepath}")
        sys.exit(1)

    return result


# ─────────────────────────────────────────────
#  Categorizer
# ─────────────────────────────────────────────

def categorize_entries(entries: list[LogEntry], filter_cat: Optional[str] = None) -> dict:
    """Group entries by status code category, optionally filtering to one."""
    categories: dict[int, list[LogEntry]] = defaultdict(list)

    for entry in entries:
        bucket = entry.status_code // 100
        categories[bucket].append(entry)

    # Apply filter
    if filter_cat:
        key = int(filter_cat[0])  # "4xx" → 4
        categories = {key: categories.get(key, [])}

    return dict(categories)


def build_code_counter(entries: list[LogEntry]) -> Counter:
    """Count occurrences of each individual status code."""
    return Counter(e.status_code for e in entries)


# ─────────────────────────────────────────────
#  Reporters
# ─────────────────────────────────────────────

def bar(count: int, total: int, width: int = 30) -> str:
    """Generate a simple ASCII progress bar."""
    filled = int(width * count / total) if total else 0
    if UNICODE_OK:
        return "\u2588" * filled + "\u2591" * (width - filled)
    return "#" * filled + "-" * (width - filled)


def report_terminal(
    result: ParseResult,
    categories: dict,
    top_n: int = 0,
    verbose: bool = False
) -> None:
    """Print a rich terminal report."""
    entries = result.entries
    total   = len(entries)
    counter = build_code_counter(entries)

    heavy = "=" if not UNICODE_OK else "\u2550"
    light = "-" if not UNICODE_OK else "\u2500"
    dash  = "--" if not UNICODE_OK else "\u2014"

    print(f"\n{BOLD}{heavy * 60}{RESET}")
    print(f"{BOLD}  HTTP Log Analyzer {dash} Summary Report{RESET}")
    print(f"{BOLD}{heavy * 60}{RESET}")
    print(f"  {DIM}Total Lines : {result.total_lines}{RESET}")
    print(f"  {DIM}Parsed      : {total}{RESET}")
    print(f"  {DIM}Skipped     : {result.skipped_lines} (malformed){RESET}")
    print(f"{BOLD}{light * 60}{RESET}\n")

    if not entries:
        print("  No matching entries found.\n")
        return

    # ── Category breakdown ──────────────────────────────────────
    for bucket in sorted(categories):
        cat_entries = categories[bucket]
        if not cat_entries:
            continue

        label, icon, color = STATUS_CATEGORIES.get(bucket, ("Unknown", "[?] ", "\033[0m"))
        cat_count = len(cat_entries)
        pct = cat_count / total * 100

        print(f"  {color}{BOLD}{icon}{label}{RESET}")
        print(f"  {bar(cat_count, total)}  {color}{cat_count:>4}{RESET}  ({pct:.1f}%)")
        print()

        # Per-code breakdown within the category
        code_counts = Counter(e.status_code for e in cat_entries)
        for code, count in sorted(code_counts.items()):
            desc = STATUS_DESCRIPTIONS.get(code, "Unknown")
            pct_code = count / total * 100
            print(f"      {color}{code}{RESET}  {desc:<28} {count:>4}  ({pct_code:.1f}%)")

        # Top paths for this category (if verbose)
        if verbose:
            path_counts = Counter(e.path for e in cat_entries)
            print(f"\n      {DIM}Top paths:{RESET}")
            for path, cnt in path_counts.most_common(3):
                print(f"        {DIM}{cnt:>4}x  {path}{RESET}")

        print(f"  {DIM}{light * 56}{RESET}\n")

    # ── Top N status codes overall ───────────────────────────────
    if top_n > 0:
        print(f"{BOLD}  Top {top_n} Status Codes (overall):{RESET}")
        for code, count in counter.most_common(top_n):
            bucket = code // 100
            _, _, color = STATUS_CATEGORIES.get(bucket, ("", "", ""))
            desc = STATUS_DESCRIPTIONS.get(code, "Unknown")
            pct = count / total * 100
            print(f"    {color}{code}{RESET}  {desc:<28}  {count:>4}  ({pct:.1f}%)")
        print()

    print(f"{BOLD}{heavy * 60}{RESET}\n")


def report_json(result: ParseResult, categories: dict) -> str:
    """Serialize the result to a JSON string."""
    total = len(result.entries)
    counter = build_code_counter(result.entries)
    output = {
        "summary": {
            "total_lines": result.total_lines,
            "parsed": total,
            "skipped": result.skipped_lines,
        },
        "categories": {},
        "status_codes": {},
    }

    for bucket, entries in sorted(categories.items()):
        label, _, _ = STATUS_CATEGORIES.get(bucket, ("Unknown", "", ""))
        output["categories"][label] = {
            "count": len(entries),
            "percentage": round(len(entries) / total * 100, 2) if total else 0,
        }

    for code, count in sorted(counter.items()):
        output["status_codes"][str(code)] = {
            "description": STATUS_DESCRIPTIONS.get(code, "Unknown"),
            "count": count,
            "percentage": round(count / total * 100, 2) if total else 0,
        }

    return json.dumps(output, indent=2)


def report_csv(result: ParseResult) -> list[list]:
    """Return CSV rows for all parsed entries."""
    headers = ["ip", "timestamp", "method", "path", "protocol",
               "status_code", "category", "description", "response_size"]
    rows = [headers]
    for e in result.entries:
        bucket = e.status_code // 100
        label, _, _ = STATUS_CATEGORIES.get(bucket, ("Unknown", "", ""))
        desc = STATUS_DESCRIPTIONS.get(e.status_code, "Unknown")
        rows.append([
            e.ip, e.timestamp, e.method, e.path, e.protocol,
            e.status_code, label, desc, e.response_size,
        ])
    return rows


# ─────────────────────────────────────────────
#  CLI Entry Point
# ─────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="log_parser",
        description=(
            "Parse and categorize HTTP status codes from an access log file.\n"
            "Supports Apache / Nginx Combined Log Format."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python log_parser.py sample.log
  python log_parser.py sample.log --filter 5xx
  python log_parser.py sample.log --filter 4xx --verbose
  python log_parser.py sample.log --top 5
  python log_parser.py sample.log --output json
  python log_parser.py sample.log --output json --save report.json
  python log_parser.py sample.log --output csv  --save report.csv
        """,
    )

    parser.add_argument(
        "logfile",
        type=Path,
        help="Path to the log file to analyze",
    )
    parser.add_argument(
        "--filter", "-f",
        choices=["1xx", "2xx", "3xx", "4xx", "5xx"],
        metavar="CATEGORY",
        help="Show only a specific status category (1xx/2xx/3xx/4xx/5xx)",
        dest="filter_cat",
    )
    parser.add_argument(
        "--top", "-t",
        type=int,
        default=0,
        metavar="N",
        help="Show the top N most frequent status codes",
    )
    parser.add_argument(
        "--output", "-o",
        choices=["terminal", "json", "csv"],
        default="terminal",
        help="Output format (default: terminal)",
    )
    parser.add_argument(
        "--save", "-s",
        type=Path,
        metavar="FILE",
        help="Save output to a file (for json/csv output formats)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show additional details like top paths per category",
    )

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    # ── Parse ────────────────────────────────────────────────────
    print(f"\n{DIM}  Parsing: {args.logfile}{RESET}")
    result = parse_log_file(args.logfile)
    categories = categorize_entries(result.entries, args.filter_cat)

    # ── Output ───────────────────────────────────────────────────
    if args.output == "terminal":
        report_terminal(result, categories, top_n=args.top, verbose=args.verbose)

    elif args.output == "json":
        output = report_json(result, categories)
        if args.save:
            args.save.write_text(output, encoding="utf-8")
            print(f"\n{BOLD}\033[92m[SAVED]{RESET} JSON report written to: {args.save}\n")
        else:
            print(output)

    elif args.output == "csv":
        rows = report_csv(result)
        if args.save:
            with open(args.save, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(rows)
            print(f"\n{BOLD}\033[92m[SAVED]{RESET} CSV report written to: {args.save}\n")
        else:
            writer = csv.writer(sys.stdout)
            writer.writerows(rows)


if __name__ == "__main__":
    main()
