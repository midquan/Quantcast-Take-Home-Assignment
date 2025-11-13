# Cookie Log Analyzer

Command-line tool that processes cookie log CSV files to find the most active cookie(s) for a given date.

## Quick Start

```bash
python most_active_cookie.py -f cookie_log.csv -d 2018-12-09
```

**Output:**
```
AtY0laUfhglK3lC7
```

## Installation

No external dependencies required. Python 3.10 or higher.

**Clone or download the repository:**
```bash
git clone <your-repo-url>
cd cookie-log-analyzer
```

**Run directly:**
```bash
python most_active_cookie.py --help
```

## Usage

```bash
python most_active_cookie.py -f <path-to-csv> -d <YYYY-MM-DD>
```

**Arguments:**
- `-f, --file` - Path to CSV file with cookie log data (required)
- `-d, --date` - Date to search in YYYY-MM-DD format (required)

**CSV Format:**

The input file must have `cookie` and `timestamp` columns:
```csv
cookie,timestamp
AtY0laUfhglK3lC7,2018-12-09T14:19:00+00:00
SAZuXPGUrfbcn5UA,2018-12-09T10:13:00+00:00
```

**Examples:**

Single most active cookie:
```bash
python most_active_cookie.py -f cookie_log.csv -d 2018-12-09
```
Output: `AtY0laUfhglK3lC7`

Multiple cookies tied for most active:
```bash
python most_active_cookie.py -f cookie_log.csv -d 2018-12-08
```
Output:
```
SAZuXPGUrfbcn5UA
4sMM2LxV07bPJzwf
fbcn5UAVanZf6UtG
```

## Exit Codes

- `0` - Success
- `1` - No cookies found for the specified date
- `2` - Error (invalid file, bad date format, etc.)

## Implementation

Uses `collections.Counter` for O(n) frequency counting. Input validation happens at argument parsing time via custom argparse type validators.

If multiple cookies are tied for the highest count, all are returned (one per line).

The script gracefully handles malformed data by skipping rows with empty cookies or timestamps, making it resilient to real-world log file quality issues.

## Testing

Install pytest and run the test suite:

```bash
pip install pytest pytest-cov
pytest test_most_active_cookie.py -v
```

The test suite includes 10 test cases covering:
- Single winner and tied winners
- Empty files and missing columns
- Malformed timestamps
- Original specification examples
- Date not found scenarios

**Run with coverage:**
```bash
pytest test_most_active_cookie.py --cov=most_active_cookie --cov-report=term-missing
```

## Requirements

**Runtime:**
- Python 3.10+
- Standard library only (no external dependencies)

**Development:**
- pytest >= 7.4.0
- pytest-cov >= 4.1.0 (optional, for coverage reports)

## Project Structure

```
.
├── most_active_cookie.py      # Main script
├── test_most_active_cookie.py # Test suite
├── cookie_log.csv             # Sample data
├── README.md                  # This file
└── requirements-dev.txt       # Development dependencies
```

## Author

**Michael Quan**

For questions or support, please open an issue in the repository.
