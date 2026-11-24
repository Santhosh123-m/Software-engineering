# Fuzz Testing Report - Lab 7

| Field | Value |
|---|---|
| Course | PES University Software Engineering Lab |
| Student ID | 24AM252|
| Project | Library Fines |
| Method | Hypothesis property-based fuzz testing with pytest |

## Objective

Use generated inputs to identify input-validation failures in `parse_member_id`, `total_fine`, and `shelf_code`, fix the application, and verify that valid behavior remains correct.

## Original Application Issues

The original functions operated directly on inputs without checking types or format:

- `parse_member_id` called `split('-')` and unpacked the result without validating the delimiter count. A `None` value caused `AttributeError`; extra delimiters failed during unpacking; malformed numbers leaked `ValueError`; and outer whitespace remained in the returned member type.
- `total_fine` called `split(',')` and `int()` without checking input type or individual fields. `None` caused `AttributeError`, empty or malformed fields leaked conversion errors, and negative values were silently treated as zero fine.
- `shelf_code` assumed a string with at least two words. `None` caused `AttributeError`, and empty or single-word titles caused `IndexError`.

## Initial Fuzz Run

The completed tests were first run against the untouched application with:

```text
python -m pytest -v test_library_fines.py
```

Hypothesis minimized unexpected-type failures to `None` for the member ID, CSV, and title functions. The invalid-title property found an empty string that caused `IndexError`. A deterministic format check also showed that member ID whitespace was not normalized, and malformed fine CSV values were not rejected consistently.

**Initial result:** 5 failed, 4 passed. The actual initial failure output is included as screenshot 02 in the PDF and `screenshots/02_initial_fuzz_failures.png`.

## Strategies and Properties

The suite uses `st.text()` to generate arbitrary Unicode and malformed strings, `st.integers()` for numeric IDs and day values, `st.none()` and `st.booleans()` for unexpected types, `st.lists()` for both generated day lists and wrong-type inputs, and `st.one_of()` to combine malformed strings with unexpected types.

Six Hypothesis properties each explore up to 120 examples:

1. Generated valid member IDs return an uppercase type and the original numeric value.
2. Malformed member IDs and unexpected types raise `ValueError`.
3. Generated valid day lists match a reference fine calculation.
4. Malformed CSV values and unexpected types raise `ValueError`.
5. Generated multiword titles return the initials of the first two words.
6. Titles with fewer than two words and unexpected types raise `ValueError`.

Deterministic checks add explicit cases for whitespace, missing or repeated delimiters, alphabetic and negative numbers, empty CSV entries, decimal values, Unicode digits, Unicode titles, punctuation, and title spacing.

## Fixes Implemented

- All three functions validate their input type and raise `ValueError` for wrong types or invalid formats.
- Member IDs are trimmed at the outside, require exactly one hyphen, require an ASCII alphabetic member type, and accept only non-negative ASCII decimal digits for the numeric ID.
- CSV input must contain at least one non-empty field. Every field must be a non-negative ASCII decimal integer; surrounding whitespace around a field is allowed.
- Fine calculations preserve the original rule of 2 per day beyond day 14.
- Title parsing uses Python's whitespace splitting and rejects fewer than two words before indexing.
- The command-line application catches validation errors per prompt, prints a clear message, and continues.

## Final Test Results

The fixed application was verified using valid examples and invalid command-line inputs. The final fuzz suite was run with:

```text
python -m pytest -v test_library_fines.py
```

**Final result:** 9 passed, 0 failed. All three functions have generated valid and malformed input coverage, including unexpected types. The final successful terminal output is included as screenshot 04 in the PDF and `screenshots/04_final_fuzz_test_results.png`.

## Conclusion

Hypothesis exposed failures at input boundaries that the original happy-path behavior did not reveal. Format and type checks now produce predictable errors, valid calculations retain their intended behavior, and the final property-based test suite passes.

