# Issues found in `library_system.py`

Baseline: Pylint 6.07/10, Bandit 2 findings (1 Medium, 1 Low), Flake8 14 findings.
After fixes: Pylint 10.00/10, Bandit 0 findings, Flake8 0 findings.
Line numbers refer to the original file. Sorted by severity (security first, then bugs, then quality/style).

| # | Issue | Type | Line(s) | Description | Fix Approach |
|---|-------|------|---------|-------------|--------------|
| 1 | `eval()` on a rule string (Bandit B307 Medium, Pylint W0123) | Security | 44-45 | `fine_from_rule` passes a caller-supplied string to `eval`, so a rule such as `__import__('os').system(...)` runs arbitrary code. | Parse the rule with `ast.parse` and evaluate only numbers and `+ - * / // %` through a whitelist. Anything else raises `ValueError`. |
| 2 | Bare `except: pass` (Bandit B110 Low, Pylint W0702, Flake8 E722) | Bug / Security | 17-22 | `return_book` hides every error, including `KeyboardInterrupt`. Returning a book nobody borrowed fails silently. | Catch only `(KeyError, ValueError)` and print which loan was not found. |
| 3 | Mutable default argument `dates=[]` (Pylint W0102) | Bug | 9-14 | The list is shared between calls. The demo prints "loan dates on record: 1, 2, 3" for three different students. | Default to `None` and create a new list inside the function. |
| 4 | Renewal changes the global fine rate (Pylint W0603) | Logic bug | 27-31 | Renewing any book for more than 14 days raised `FINE_PER_DAY` for all students. The demo's 5-day fine rose from 10 to 15. | Remove the `global` and the side effect. `renew_book` only records the renewal. |
| 5 | Negative days give a negative fine | Logic bug (no tool flags it) | 24-25 | `calculate_fine(-3)` returned -9, which credits money to the student. | Clamp with `max(days_overdue, 0)`. |
| 6 | Non-string book id accepted | Logic bug (no tool flags it) | 56 | `add_book_loan("S103", 4521)` stored an int, and `renewBook` would crash when concatenating it to a string. | Reject non-string ids with a message. |
| 7 | Empty student id silently ignored | Logic bug (no tool flags it) | 10-11 | The function returns with no feedback, so the loan is lost without any message. | Print "Loan rejected: missing student id". |
| 8 | File opened without `with` or encoding (Pylint R1732, W1514) | Bug / Quality | 33-42 | The handle leaks if `json.loads` or `write` raises, and the encoding depends on the platform. | Use `with open(..., encoding="utf-8")` and `json.load` / `json.dump`. |
| 9 | `global loans` reassignment (Pylint W0603) | Quality | 35 | `load_records` rebinds a module global. | Mutate in place with `loans.clear()` and `loans.update(data)`. |
| 10 | Non-numeric input crashes the program | Bug (no tool flags it) | 63 | `int(days)` raises `ValueError` on input like `abc`. | Wrap in `try/except ValueError` and print a message. |
| 11 | Unused import `os` (Pylint W0611, Flake8 F401) | Quality | 2 | Dead import. | Remove it. |
| 12 | `renewBook` naming (Pylint C0103) | Style | 27 | Not snake_case. | Rename to `renew_book` and update the caller. |
| 13 | Missing docstrings (Pylint C0114, C0116) | Style | many | The module and every function lack documentation. | Add short docstrings. |
| 14 | `%` and `+` string building (Pylint C0209) | Style | 14, 31 | Old formatting style. | Use f-strings. |
| 15 | `main()` runs on import | Quality | 68 | Importing the module runs the demo and blocks on `input()`. | Add `if __name__ == "__main__":`. |
| 16 | Blank lines and long lines (Flake8 E302, E305, E501) | Style | 9-68 | 12 blank-line violations and 2 lines over 79 characters. | Add 2 blank lines around top-level definitions and wrap the long lines. |

## Commits (local, not pushed)

1. Fix Bandit findings: #1 and #2.
2. Fix Pylint findings and logic bugs: #3-#15.
3. Fix Flake8 formatting: #16, plus the before/after reports and these notes.
