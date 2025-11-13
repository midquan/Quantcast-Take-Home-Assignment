#!/usr/bin/env python3

import sys
import csv
import argparse
import os
from collections import Counter
from datetime import datetime

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("-f", "--file", dest="csv_path", required=True, type=str)
    p.add_argument("-d", "--date", required=True)
    args = p.parse_args()
    
    if not os.path.exists(args.csv_path):
        p.error(f"File '{args.csv_path}' not found")
    
    try:
        with open(args.csv_path, 'r') as f:
            reader = csv.DictReader(f)
            next(reader)
            if 'cookie' not in reader.fieldnames or 'timestamp' not in reader.fieldnames:
                p.error(f"CSV must have 'cookie' and 'timestamp' columns")
    except csv.Error:
        p.error(f"Invalid CSV file format")
    except Exception as e:
        p.error(f"Error reading file: {e}")
    
    try:
        datetime.strptime(args.date, '%Y-%m-%d')
    except ValueError:
        p.error(f"Date must be in YYYY-MM-DD format, got '{args.date}'")
    
    return args


def find_most_active(csv_path, date_str):
    cookie_counts = Counter()
    
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            timestamp = row['timestamp']
            if timestamp.startswith(date_str):
                cookie_counts[row['cookie']] += 1
    
    if not cookie_counts:
        return None
    
    max_count = max(cookie_counts.values())
    most_active = [cookie for cookie, count in cookie_counts.items() if count == max_count]
    
    return most_active


def main():
    args = parse_args()
    result = find_most_active(args.csv_path, args.date)
    if result is None:
        return 0
    try:
        iter(result)
    except TypeError:
        print(result)
    else:
        for item in result:
            print(item)


if __name__ == "__main__":
    sys.exit(main() or 0)