# Design Decisions & Interview Notes

## 1. Validation Strategy: Custom Argparse Type Validators

**Approach:** Created `validate_csv_file()` and `validate_date_format()` as custom type validators in argparse.

**Why:**
- Fail fast with clear error messages
- Cleaner separation of concerns
- Standard Python idiom for CLI argument validation

**Time Complexity:** O(1)

## 2. Algorithm Choice: Counter + Two-Phase Approach

**Approach:** Used `collections.Counter` for frequency counting, followed by finding the maximum and filtering.

**Why:**
- Counter is implemented in C, providing optimal performance
- Clear two-phase logic: count, then filter
- Simple handling of ties
- More readable than tracking max during iteration

**Alternative Rejected:** Tracking max during the counting loop would require `cookie not in most_active` checks. Since `most_active` would be a list, this is O(m) per check where m is the number of tied cookies. This approach is less predictable and harder to reason about than the clean two-phase approach.

**Time Complexity:** O(n + k) where n = rows, k = unique cookies
**Space Complexity:** O(k)

## 3. Date Filtering: String Prefix Matching

**Approach:** Used `timestamp.startswith(date_str)` instead of full datetime parsing.

**Why:**
- ISO 8601 timestamps sort lexicographically
- String comparison is O(1) and avoids parsing overhead
- Simple and correct for date-based filtering

**Time Complexity:** O(1) per comparison

## 4. Error Handling: Specific Exceptions

**Approach:** Caught specific exceptions (`FileNotFoundError`, `PermissionError`, `csv.Error`) with descriptive messages.

**Why:**
- Better debugging and user experience
- Distinguishes between different failure modes
- Follows Python best practices

## 5. Return Value: None vs Empty List

**Approach:** Return `None` when no cookies found, rather than empty list.

**Why:**
- `None` clearly indicates "no data exists for this date"
- Allows `main()` to distinguish between no results vs. error states
- Explicit handling forces caller to consider the no-data case

## Interview Talking Points

### "Why not use pandas?"
Pandas adds 100+ MB of dependencies for a simple task. The csv module is sufficient and keeps the tool lightweight.

### "Why Counter over dict?"
Counter is optimized for frequency counting with cleaner syntax and C-level performance. It automatically handles missing keys and provides convenient methods.

### "How would you handle huge files?"
Current implementation uses O(k) memory where k = unique cookies, not O(n) for total rows. For truly massive files, consider chunked processing with pandas or a database approach.

### "What about timezones?"
The implementation uses string prefix matching, which is timezone-agnostic. If timezone normalization were required, parse with `datetime.fromisoformat()` and convert to UTC.
