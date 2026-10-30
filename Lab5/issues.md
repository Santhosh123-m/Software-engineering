# Lab 5: Static Code Analysis — Issues Report

## Project: Applicant Tracking System

### Tools Used
- Pylint
- Bandit
- Flake8

## Issues Identified and Fixed

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| SQL Injection Risk (B608) | Security — Medium | 8 | The SQL INSERT query used an f-string to insert applicant data directly into the query, creating a potential SQL injection vulnerability. | Replaced the f-string with a parameterized SQL query using placeholders (`?`). |
| Unsafe Use of eval() (B307) | Security — Medium | 14 | The `eval()` function evaluated the salary rule as Python code, which could execute unintended expressions. | Replaced `eval()` with input validation using a regular expression and safe integer parsing. |
| Broad Exception Handling (B110) | Error Handling — Low | 28–29 | The code caught every exception and silently ignored it using `pass`, making errors difficult to detect. | Removed the broad exception handler and added explicit handling for an applicant ID that does not exist. |
| Unused Variable | Code Quality | 15 | The variable `total_seen` was assigned a value but never used. | Removed the unnecessary variable. |
| Missing Module and Function Docstrings | Code Quality | 1, 7, 12, 24, 31, 38, 42 | The module and functions lacked documentation describing their purpose. | Added a module docstring and docstrings for all functions. |
| Invalid Function Naming | Code Quality | 7, 24, 31, 38 | Function names such as `addApplicant`, `updateStatus`, `exportReport`, and `countByStatus` did not follow Python's snake_case naming convention. | Renamed them to `add_applicant`, `update_status`, `export_report`, and `count_by_status`. |
| Long Lines and Trailing Whitespace | Code Style | Multiple | Several lines exceeded the recommended length, and one line contained trailing whitespace. | Split long statements across multiple lines and removed trailing whitespace. |
| Inconsistent Return Statements | Code Quality | 12–21 | The `shortlist()` function returned a result only when the list was non-empty, so it implicitly returned `None` otherwise. | Updated the function to always return a list, including an empty list when no applicants qualify. |
| Unsafe File Handling | Code Quality | 32–34 | The report file was opened without explicitly specifying an encoding and was manually closed. The comma-separated output was also constructed manually. | Used a `with open()` context manager with UTF-8 encoding and Python's `csv.writer`. |
| Missing Blank Lines | Code Style | 30 | There was insufficient blank-line spacing between function definitions. | Added the required blank lines between top-level functions. |

## Verification After Fixing

| Tool | Original Result | Final Result |
|---|---|---|
| Pylint | 4.47/10 | 10.00/10 |
| Bandit | 2 Medium and 1 Low severity issue | No issues identified |
| Flake8 | Multiple style violations | No violations reported |

## Conclusion

Static code analysis helped identify security risks, code quality problems, and style violations in the Applicant Tracking System. After applying the fixes, the program retained its intended functionality, the Pylint score improved to 10.00/10, Bandit reported no issues, and Flake8 reported no violations.