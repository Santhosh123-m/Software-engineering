# Reflection

## 1. Which issues were the easiest and which were the hardest to fix?
Easiest: the style findings. Removing the unused import, renaming `renewBook`, adding docstrings, switching to f-strings and fixing blank lines were mechanical, and the tool tells you the fix.
Hardest: `eval`. Deleting it would break `fine_from_rule`, so I had to design a replacement: an `ast`-based evaluator that only allows numbers and basic arithmetic. The renewal bug was also hard because I had to decide what the code was meant to do. A renewal that raises the fine rate for every student is clearly wrong, but no tool says so.

## 2. Did the tools report false positives, or miss real problems?
There were no true false positives, but the severities do not match the real risk. Bandit rated the bare `except: pass` as Low, yet it hid real errors. Pylint's missing-docstring messages made up most of the report but say little about correctness.
The tools missed five real bugs that I only found by running the program and reading the output: negative days giving a negative fine, an integer book id accepted, an empty student id silently dropped, the renewal changing the global fine rate, and a crash on non-numeric input. Static analysis checks patterns, not intent.

## 3. How would you integrate static analysis into your development workflow?
I would run Flake8 and Pylint in an editor plugin or a pre-commit hook so problems show up while writing. Bandit and Pylint would run as CI checks on every pull request, with a minimum Pylint score and no Medium or High Bandit findings. They would sit alongside unit tests and code review, not replace them. Intentional exceptions should be suppressed narrowly, with a comment explaining why.

## 4. What improvements in quality, readability and security did you see?
Pylint went from 6.07 to 10.00, Bandit from 2 findings to 0, and Flake8 from 14 findings to 0. The code is safer, with no arbitrary-code execution through `eval` and no swallowed errors. It is also more predictable: no shared mutable default, no hidden global changes, and files are always closed. It is easier to read, with docstrings, consistent names and PEP 8 formatting. The behaviour is still the same demo, now with correct fines and clear messages for bad input.
