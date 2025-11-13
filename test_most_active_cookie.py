import pytest
import subprocess
import sys

@pytest.fixture
def create_csv_file(tmp_path):
    """A pytest fixture to create a CSV file in a temporary directory."""
    def _create_csv_file(filename, content):
        file_path = tmp_path / filename
        file_path.write_text(content)
        return str(file_path)
    return _create_csv_file

def run_script(args):
    """Helper function to run the main script with mocked arguments."""
    process = subprocess.run(
        [sys.executable, "most_active_cookie.py"] + args,
        capture_output=True,
        text=True
    )
    return process.stdout.strip().splitlines(), process.stderr.strip(), process.returncode

def test_clear_winner(create_csv_file):
    """Test case with a single most active cookie."""
    csv_content = (
        "cookie,timestamp\n"
        "pbOLF3QajQsCmHUq,2025-11-12T10:00:00+00:00\n"
        "pbOLF3QajQsCmHUq,2025-11-12T11:00:00+00:00\n"
        "hupHAct4T0qsQd2i,2025-11-12T12:00:00+00:00\n"
        "pbOLF3QajQsCmHUq,2025-11-12T13:00:00+00:00\n"
        "MyxO3k4ja5N1qUT3,2025-11-11T10:00:00+00:00"
    )
    csv_path = create_csv_file("test1.csv", csv_content)
    
    output, stderr, exit_code = run_script(["-f", csv_path, "-d", "2025-11-12"])
    
    assert exit_code == 0, f"Exit code was {exit_code}, stderr: {stderr}"
    assert sorted(output) == ["pbOLF3QajQsCmHUq"]

def test_tied_winners(create_csv_file):
    """Test case with multiple cookies tied for the most active."""
    csv_content = (
        "cookie,timestamp\n"
        "sJcZT3VIgEV2xKQb,2025-11-12T08:00:00+00:00\n"
        "OnUv9UEGxdJQV7kw,2025-11-12T08:30:00+00:00\n"
        "sJcZT3VIgEV2xKQb,2025-11-12T09:00:00+00:00\n"
        "OnUv9UEGxdJQV7kw,2025-11-12T09:30:00+00:00\n"
        "hycDmBapFD9y5Vmy,2025-11-12T10:00:00+00:00"
    )
    csv_path = create_csv_file("test2.csv", csv_content)
    
    output, stderr, exit_code = run_script(["-f", csv_path, "-d", "2025-11-12"])
    
    assert exit_code == 0, f"Exit code was {exit_code}, stderr: {stderr}"
    assert sorted(output) == sorted(["OnUv9UEGxdJQV7kw", "sJcZT3VIgEV2xKQb"])

def test_no_results(create_csv_file):
    """Test case where no cookies are found for the given date."""
    csv_content = (
        "cookie,timestamp\n"
        "6xHusAPBEaFIwRjw,2025-11-10T12:00:00+00:00\n"
        "UvVEplqNureNQ6U9,2025-11-11T14:00:00+00:00"
    )
    csv_path = create_csv_file("test3.csv", csv_content)
    
    output, stderr, exit_code = run_script(["-f", csv_path, "-d", "2025-11-12"])
    
    assert exit_code == 1, f"Exit code was {exit_code}, stderr: {stderr}"
    assert output == []
    assert "No cookies found for date: 2025-11-12" in stderr

def test_file_not_found():
    """Test case where the CSV file does not exist."""
    output, stderr, exit_code = run_script(["-f", "non_existent_file.csv", "-d", "2025-11-12"])
    
    assert exit_code == 2
    assert "File 'non_existent_file.csv' does not exist" in stderr

def test_invalid_date_format():
    """Test case with an invalid date format."""
    output, stderr, exit_code = run_script(["-f", "cookie_log.csv", "-d", "2025/11/12"])
    
    assert exit_code == 2
    assert "Date must be in %Y-%m-%d format" in stderr

def test_original_cookie_log_dec_09(create_csv_file):
    """Test with original cookie_log.csv data for 2018-12-09."""
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
    
    assert exit_code == 0, f"Exit code was {exit_code}, stderr: {stderr}"
    assert output == ["AtY0laUfhglK3lC7"]

def test_original_cookie_log_dec_08(create_csv_file):
    """Test with original cookie_log.csv data for 2018-12-08."""
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
    
    assert exit_code == 0, f"Exit code was {exit_code}, stderr: {stderr}"
    assert sorted(output) == sorted(["4sMM2LxV07bPJzwf", "SAZuXPGUrfbcn5UA", "fbcn5UAVanZf6UtG"])

def test_empty_csv(create_csv_file):
    """Test case with only headers, no data rows."""
    csv_content = "cookie,timestamp"
    csv_path = create_csv_file("empty.csv", csv_content)
    
    output, stderr, exit_code = run_script(["-f", csv_path, "-d", "2025-11-12"])
    
    assert exit_code == 1
    assert "No cookies found" in stderr

def test_malformed_timestamp(create_csv_file):
    """Test case with malformed timestamp (should skip row gracefully)."""
    csv_content = (
        "cookie,timestamp\n"
        "validCookie,2025-11-12T10:00:00+00:00\n"
        "badCookie,invalid-timestamp\n"
        "validCookie,2025-11-12T11:00:00+00:00"
    )
    csv_path = create_csv_file("malformed.csv", csv_content)
    
    output, stderr, exit_code = run_script(["-f", csv_path, "-d", "2025-11-12"])
    
    assert exit_code == 0
    assert output == ["validCookie"]

def test_missing_cookie_column(create_csv_file):
    """Test CSV missing required cookie column."""
    csv_content = "timestamp\n2025-11-12T10:00:00+00:00"
    csv_path = create_csv_file("missing_col.csv", csv_content)
    
    output, stderr, exit_code = run_script(["-f", csv_path, "-d", "2025-11-12"])
    
    assert exit_code == 2
    assert "Missing required columns: cookie" in stderr
