# Day 5 — HTTP Log Parser CLI Tool

> **SDET + AI Mastery | Month 1 / Week 1 / Day 5**

A command-line tool to parse Apache/Nginx-style HTTP access log files, categorize status codes, and generate summary reports in multiple formats.

---

## Project Structure

```
Day_5/
├── log_parser.py   # Main CLI tool
├── sample.log      # Sample log file for testing
└── README.md       # This file
```

---

## Features

| Feature | Description |
|---|---|
| **Parsing** | Regex-based parsing of Combined Log Format |
| **Categorization** | Groups entries into 1xx / 2xx / 3xx / 4xx / 5xx |
| **Filtering** | `--filter 4xx` to focus on a specific category |
| **Top-N** | `--top 5` to show most frequent status codes |
| **Verbose** | `--verbose` shows top paths per category |
| **Output Formats** | Terminal (rich), JSON, CSV |
| **File Export** | `--save report.json` / `--save report.csv` |
| **Error Handling** | Gracefully skips malformed lines |

---

## Usage

```bash
# Basic report (terminal output)
python log_parser.py sample.log

# Filter to server errors only
python log_parser.py sample.log --filter 5xx

# Show top 5 most frequent codes + verbose path details
python log_parser.py sample.log --top 5 --verbose

# Export to JSON
python log_parser.py sample.log --output json --save report.json

# Export to CSV
python log_parser.py sample.log --output csv --save report.csv

# Filter 4xx errors and save as JSON
python log_parser.py sample.log --filter 4xx --output json --save 4xx_errors.json
```

---

## Log Format Supported

Standard **Apache / Nginx Combined Log Format**:

```
IP - user [timestamp] "METHOD /path HTTP/1.1" STATUS SIZE "referer" "agent"
```

Example:
```
192.168.1.1 - alice [08/May/2026:12:00:01 +0000] "GET /index.html HTTP/1.1" 200 1024 "-" "Mozilla/5.0"
```

---

## Architecture

```
log_parser.py
│
├── LogEntry (dataclass)      — represents one parsed line
├── ParseResult (dataclass)   — holds all entries + parse stats
│
├── parse_log_file()          — reads file, applies regex, builds entries
├── categorize_entries()      — groups entries by 1xx–5xx bucket
├── build_code_counter()      — counts per-code occurrences
│
├── report_terminal()         — rich colored terminal output
├── report_json()             — JSON serialization
├── report_csv()              — CSV rows for all entries
│
└── main()                    — argparse CLI entry point
```

---

## Key Concepts Practiced

- **`argparse`** — building a real CLI with flags, choices, and help text
- **`re` (regex)** — named capture groups to parse structured text
- **`dataclasses`** — clean typed data structures
- **`collections.Counter` / `defaultdict`** — frequency analysis
- **`pathlib.Path`** — modern file I/O
- **`json` / `csv`** — multiple output format support
- **ANSI escape codes** — terminal color output without third-party libs
- **Graceful error handling** — skipping malformed lines, file not found

---

## Sample Output

```
════════════════════════════════════════════════════════════
  HTTP Log Analyzer — Summary Report
════════════════════════════════════════════════════════════
  Total Lines : 26
  Parsed      : 25
  Skipped     : 1 (malformed)
────────────────────────────────────────────────────────────

  ✅ 2xx Success
  █████████████░░░░░░░░░░░░░░░░░    9  (36.0%)

      200  OK                            8  (32.0%)
      204  No Content                    1  (4.0%)

  ...

  ❌ 5xx Server Error
  ████░░░░░░░░░░░░░░░░░░░░░░░░░░    4  (16.0%)

      500  Internal Server Error         2  (8.0%)
      502  Bad Gateway                   1  (4.0%)
      503  Service Unavailable           1  (4.0%)
════════════════════════════════════════════════════════════
```
