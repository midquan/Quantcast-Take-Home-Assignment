import pytest
import sys
import csv
from pathlib import Path
from unittest.mock import patch
from io import StringIO

# Import the module to test
import most_active_cookie


@pytest.fixture
def create_csv_file(tmp_path):
    def _create_csv(filename, content):
        csv_path = tmp_path / filename
        csv_path.write_text(content)
        return str(csv_path)
    return _create_csv


def run_script(args):
    """Helper function to run the main script with mocked arguments."""
    with patch('sys.argv', ['most_active_cookie.py'] + args):
        stdout_capture = StringIO()
        stderr_capture = StringIO()
        
        with patch('sys.stdout', stdout_capture), patch('sys.stderr', stderr_capture):
            try:
                exit_code = most_active_cookie.main()
            except SystemExit as e:
                exit_code = e.code
        
        stdout = stdout_capture.getvalue()
        stderr = stderr_capture.getvalue()
        
        output = stdout.strip().split('\n') if stdout.strip() else []
        return output, stderr, exit_code or 0


def test_clear_winner(create_csv_file):
    csv_content = (
        "cookie,timestamp\n"
        "pbOLF3QajQsCmHUq,2025-11-10T12:00:00+00:00\n"
        "6xHusAPBEaFIwRjw,2025-11-10T13:00:00+00:00\n"
        "pbOLF3QajQsCmHUq,2025-11-10T14:00:00+00:00\n"
        "pbOLF3QajQsCmHUq,2025-11-10T15:00:00+00:00"
    )
    csv_path = create_csv_file("test_winner.csv", csv_content)
    
    output, stderr, exit_code = run_script(["-f", csv_path, "-d", "2025-11-10"])
    
    assert exit_code == 0
    assert output == ["pbOLF3QajQsCmHUq"]
    assert stderr == ""


def test_tied_winners(create_csv_file):
    csv_content = (
        "cookie,timestamp\n"
        "cookieA,2025-11-11T12:00:00+00:00\n"
        "cookieB,2025-11-11T13:00:00+00:00\n"
        "cookieA,2025-11-11T14:00:00+00:00\n"
        "cookieB,2025-11-11T15:00:00+00:00"
    )
    csv_path = create_csv_file("test_tie.csv", csv_content)
    
    output, stderr, exit_code = run_script(["-f", csv_path, "-d", "2025-11-11"])
    
    assert exit_code == 0
    assert sorted(output) == sorted(["cookieA", "cookieB"])
    assert stderr == ""


def test_no_results(create_csv_file):
    csv_content = (
        "cookie,timestamp\n"
        "6xHusAPBEaFIwRjw,2025-11-10T12:00:00+00:00\n"
        "UvVEplqNureNQ6U9,2025-11-11T14:00:00+00:00"
    )
    csv_path = create_csv_file("test_no_cookies.csv", csv_content)
    
    output, stderr, exit_code = run_script(["-f", csv_path, "-d", "2025-11-12"])
    
    assert exit_code == 1
    assert output == []
    assert "No cookies found for date: 2025-11-12" in stderr


def test_file_not_found():
    output, stderr, exit_code = run_script(["-f", "nonexistent.csv", "-d", "2025-11-12"])
    
    assert exit_code == 2
    assert "does not exist" in stderr


def test_invalid_date_format(create_csv_file):
    """Test invalid date format - file must exist first for date validation to run."""
    csv_content = "cookie,timestamp\ntest,2025-11-10T12:00:00+00:00"
    csv_path = create_csv_file("test.csv", csv_content)
    
    output, stderr, exit_code = run_script(["-f", csv_path, "-d", "2025/11/12"])
    
    assert exit_code == 2
    assert "Date must be in" in stderr


def test_original_cookie_log_dec_09(create_csv_file):
    csv_content = (
        "cookie,timestamp\n"
        "AtY0laUfhglK3lC7,2018-12-09T14:19:00+00:00\n"
        "SAZuXPGUrfbcn5UA,2018-12-09T10:13:00+00:00\n"
        "5UAVanZf6UtGyKVS,2018-12-09T07:25:00+00:00\n"
        "AtY0laUfhglK3lC7,2018-12-09T06:19:00+00:00\n"
        "SAZuXPGUrfbcn5UA,2018-12-08T22:03:00+00:00\n"
        "4sMM2LxV07bPJzwf,2018-12-08T21:30:00+00:00\n"
        "fbcn5UAVanZf6UtG,2018-12-08T09:30:00+00:00\n"
        "4sMM2LxV07bPJzwf,2018-12-07T23:30:00+00:00"
    )
    csv_path = create_csv_file("cookie_log.csv", csv_content)
    
    output, stderr, exit_code = run_script(["-f", csv_path, "-d", "2018-12-09"])
    
    assert exit_code == 0
    assert output == ["AtY0laUfhglK3lC7"]


def test_original_cookie_log_dec_08(create_csv_file):
    """Test for 2018-12-08: SAZuXPGUrfbcn5UA, 4sMM2LxV07bPJzwf, and fbcn5UAVanZf6UtG each appear once."""
    csv_content = (
        "cookie,timestamp\n"
        "AtY0laUfhglK3lC7,2018-12-09T14:19:00+00:00\n"
        "SAZuXPGUrfbcn5UA,2018-12-09T10:13:00+00:00\n"
        "5UAVanZf6UtGyKVS,2018-12-09T07:25:00+00:00\n"
        "AtY0laUfhglK3lC7,2018-12-09T06:19:00+00:00\n"
        "SAZuXPGUrfbcn5UA,2018-12-08T22:03:00+00:00\n"
        "4sMM2LxV07bPJzwf,2018-12-08T21:30:00+00:00\n"
        "fbcn5UAVanZf6UtG,2018-12-08T09:30:00+00:00\n"
        "4sMM2LxV07bPJzwf,2018-12-07T23:30:00+00:00"
    )
    csv_path = create_csv_file("cookie_log.csv", csv_content)
    
    output, stderr, exit_code = run_script(["-f", csv_path, "-d", "2018-12-08"])
    
    assert exit_code == 0
    assert len(output) == 3
    assert "SAZuXPGUrfbcn5UA" in output
    assert "4sMM2LxV07bPJzwf" in output
    assert "fbcn5UAVanZf6UtG" in output


def test_empty_csv(create_csv_file):
    csv_content = "cookie,timestamp\n"
    csv_path = create_csv_file("empty.csv", csv_content)
    
    output, stderr, exit_code = run_script(["-f", csv_path, "-d", "2025-11-12"])
    
    assert exit_code == 1
    assert "No cookies found" in stderr


def test_malformed_timestamp(create_csv_file):
    csv_content = (
        "cookie,timestamp\n"
        "goodCookie,2025-11-10T12:00:00+00:00\n"
        "badCookie,invalid-timestamp\n"
        "goodCookie,2025-11-10T13:00:00+00:00"
    )
    csv_path = create_csv_file("malformed.csv", csv_content)
    
    output, stderr, exit_code = run_script(["-f", csv_path, "-d", "2025-11-10"])
    
    assert exit_code == 0
    assert output == ["goodCookie"]


def test_missing_cookie_column(create_csv_file):
    csv_content = (
        "timestamp\n"
        "2025-11-10T12:00:00+00:00"
    )
    csv_path = create_csv_file("missing_column.csv", csv_content)
    
    output, stderr, exit_code = run_script(["-f", csv_path, "-d", "2025-11-10"])
    
    assert exit_code == 2
    assert "Missing required columns" in stderr


def test_not_a_file(tmp_path):
    """Test that a directory path is rejected (line 44)."""
    dir_path = tmp_path / "not_a_file.csv"
    dir_path.mkdir()
    
    output, stderr, exit_code = run_script(["-f", str(dir_path), "-d", "2025-11-12"])
    
    assert exit_code == 2
    assert "is not a file" in stderr


def test_not_csv_extension(create_csv_file):
    """Test that non-.csv files are rejected (line 46)."""
    txt_content = "cookie,timestamp\ntest,2025-11-10T12:00:00+00:00"
    txt_path = create_csv_file("test.txt", txt_content)
    
    output, stderr, exit_code = run_script(["-f", txt_path, "-d", "2025-11-12"])
    
    assert exit_code == 2
    assert "File must be a CSV file" in stderr


def test_permission_error(create_csv_file, tmp_path):
    """Test permission denied error (line 142)."""
    csv_content = "cookie,timestamp\ntest,2025-11-10T12:00:00+00:00"
    csv_path = create_csv_file("protected.csv", csv_content)
    
    with patch('builtins.open', side_effect=PermissionError("Permission denied")):
        with patch('most_active_cookie.validate_csv_file', return_value=csv_path):
            output, stderr, exit_code = run_script(["-f", csv_path, "-d", "2025-11-10"])
    
    assert exit_code == 2
    assert "permission denied" in stderr.lower()


def test_csv_error(create_csv_file):
    """Test CSV parsing error (line 144)."""
    csv_path = create_csv_file("malformed.csv", "cookie,timestamp\n")
    
    with patch('csv.DictReader') as mock_reader:
        mock_instance = mock_reader.return_value
        mock_instance.fieldnames = ['cookie', 'timestamp']
        mock_instance.__iter__.side_effect = csv.Error("Bad CSV format")
        
        with patch('most_active_cookie.validate_csv_file', return_value=csv_path):
            output, stderr, exit_code = run_script(["-f", csv_path, "-d", "2025-11-10"])
    
    assert exit_code == 2
    assert "Invalid CSV format" in stderr


def test_keyboard_interrupt():
    """Test KeyboardInterrupt handling (line 181-182)."""
    with patch('most_active_cookie.parse_args', side_effect=KeyboardInterrupt()):
        output, stderr, exit_code = run_script(["-f", "test.csv", "-d", "2025-11-10"])
    
    assert exit_code == 2
    assert "Operation cancelled by user" in stderr


def test_empty_csv_file(create_csv_file):
    """Test completely empty CSV file (line 117)."""
    csv_path = create_csv_file("empty_file.csv", "")
    
    output, stderr, exit_code = run_script(["-f", csv_path, "-d", "2025-11-10"])
    
    assert exit_code == 2
    assert "CSV file is empty" in stderr


def test_missing_timestamp_column(create_csv_file):
    """Test CSV missing timestamp column (line 131)."""
    csv_content = (
        "cookie\n"
        "testCookie"
    )
    csv_path = create_csv_file("missing_timestamp.csv", csv_content)
    
    output, stderr, exit_code = run_script(["-f", csv_path, "-d", "2025-11-10"])
    
    assert exit_code == 2
    assert "Missing required columns" in stderr
    assert "timestamp" in stderr


def test_empty_cookie_value(create_csv_file):
    """Test row with empty cookie value gets skipped (line 138)."""
    csv_content = (
        "cookie,timestamp\n"
        ",2025-11-10T12:00:00+00:00\n"
        "validCookie,2025-11-10T13:00:00+00:00"
    )
    csv_path = create_csv_file("empty_cookie.csv", csv_content)
    
    output, stderr, exit_code = run_script(["-f", csv_path, "-d", "2025-11-10"])
    
    assert exit_code == 0
    assert output == ["validCookie"]


def test_empty_timestamp_value(create_csv_file):
    """Test row with empty timestamp value gets skipped (line 138)."""
    csv_content = (
        "cookie,timestamp\n"
        "testCookie,\n"
        "validCookie,2025-11-10T13:00:00+00:00"
    )
    csv_path = create_csv_file("empty_timestamp.csv", csv_content)
    
    output, stderr, exit_code = run_script(["-f", csv_path, "-d", "2025-11-10"])
    
    assert exit_code == 0
    assert output == ["validCookie"]
