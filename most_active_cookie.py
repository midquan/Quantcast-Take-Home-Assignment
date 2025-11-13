#!/usr/bin/env python3
"""
Cookie log analyzer that finds the most active cookie(s) for a given date.

Usage:
    python most_active_cookie.py -f <CSV_PATH> -d <DATE>

Arguments:
    -f, --file <CSV_PATH>: Path to the cookie log CSV file
    -d, --date <DATE>: Date in YYYY-MM-DD format

Example:
    python most_active_cookie.py -f cookie_log.csv -d 2018-12-09
"""

import sys
import csv
import argparse
from pathlib import Path
from collections import Counter
from datetime import datetime


DATE_FORMAT = '%Y-%m-%d'
REQUIRED_HEADERS = {'cookie', 'timestamp'}


def validate_csv_file(filepath: str) -> str:
    """Validate that the file exists and is readable.
    
    Args:
        filepath: Path to the CSV file
        
    Returns:
        str: Validated file path
        
    Raises:
        argparse.ArgumentTypeError: If file doesn't exist or isn't a file
    """
    path = Path(filepath)
    if not path.exists():
        raise argparse.ArgumentTypeError(f"File '{filepath}' does not exist")
    if not path.is_file():
        raise argparse.ArgumentTypeError(f"'{filepath}' is not a file")
    if not path.suffix == '.csv':
        raise argparse.ArgumentTypeError(f"File must be a CSV file, got '{path.suffix}'")
    return str(path)


def validate_date_format(date_str: str) -> str:
    """Validate that the date string is in YYYY-MM-DD format.
    
    Args:
        date_str: Date string to validate
        
    Returns:
        str: Validated date string
        
    Raises:
        argparse.ArgumentTypeError: If date format is invalid
    """
    try:
        datetime.strptime(date_str, DATE_FORMAT)
        return date_str
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Date must be in {DATE_FORMAT} format, got '{date_str}'"
        )


def parse_args() -> argparse.Namespace:
    """Parse and validate command-line arguments.
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description='Find the most active cookie(s) for a given date'
    )
    parser.add_argument(
        '-f', '--file',
        dest='csv_path',
        type=validate_csv_file,
        required=True,
        help='Path to CSV file containing cookie log data'
    )
    parser.add_argument(
        '-d', '--date',
        type=validate_date_format,
        required=True,
        help=f'Date to search in {DATE_FORMAT} format'
    )
    return parser.parse_args()


def find_most_active(csv_path: str, date_str: str) -> list[str] | None:
    """Find the most active cookie(s) for a given date.
    
    Args:
        csv_path: Path to the CSV file
        date_str: Date string in YYYY-MM-DD format
        
    Returns:
        list[str] | None: List of cookie IDs with the highest count, or None if no data found
        
    Raises:
        ValueError: If CSV is malformed or missing required columns
    """
    cookie_counts = Counter()
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            # Validate CSV structure
            if not reader.fieldnames:
                raise ValueError("CSV file is empty")
            
            # Check for required headers
            missing_headers = REQUIRED_HEADERS - set(reader.fieldnames)
            if missing_headers:
                raise ValueError(f"Missing required columns: {', '.join(missing_headers)}")
            
            # Process rows
            for row_num, row in enumerate(reader, start=2):
                cookie = row.get('cookie', '').strip()
                timestamp = row.get('timestamp', '').strip()
                
                # Skip rows with missing data
                if not cookie or not timestamp:
                    continue
                
                # Filter by date
                if timestamp.startswith(date_str):
                    cookie_counts[cookie] += 1
    
    except FileNotFoundError:
        raise ValueError(f"CSV file not found: {csv_path}")
    except PermissionError:
        raise ValueError(f"Cannot read CSV file (permission denied): {csv_path}")
    except csv.Error as e:
        raise ValueError(f"Invalid CSV format: {e}")
    
    # Return None if no cookies found for the date
    if not cookie_counts:
        return None
    
    # Find all cookies with the maximum count
    max_count = max(cookie_counts.values())
    most_active = [
        cookie for cookie, count in cookie_counts.items() 
        if count == max_count
    ]
    
    return most_active


def main() -> int:
    """Main entry point for the script.
    
    Returns:
        int: Exit code (0 for success, 1 for no data, 2 for errors)
    """
    try:
        args = parse_args()
        result = find_most_active(args.csv_path, args.date)
        
        if result is None:
            print(f"No cookies found for date: {args.date}", file=sys.stderr)
            return 1
        
        for cookie in result:
            print(cookie)
        
        return 0
    
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
