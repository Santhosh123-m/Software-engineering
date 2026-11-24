Lab 7 - Fuzz Testing with Hypothesis
This project hardens the PES University Library Fines example by testing its three input functions with property-based fuzzing, then handling malformed inputs consistently.

Objective
Fuzz testing feeds a function a wide range of valid, malformed, boundary, and unexpected inputs. It helps expose failures that a short list of hand-written examples can miss. This lab uses Hypothesis to generate and shrink test cases automatically.

Functions
parse_member_id(member_id) accepts an ID such as STU-1023 and returns ("STU", 1023). It trims outer whitespace, requires one hyphen, an ASCII letter member type, and a non-negative ASCII integer ID.
total_fine(days_csv) accepts a comma-separated list of non-negative integer days. It charges 2 per day for each book kept beyond 14 days.
shelf_code(title) returns the uppercase first letters of the first two whitespace-separated title words.
Invalid input, including an unexpected input type, raises ValueError with a specific message. The interactive application catches that error and prints a readable validation message.

Bugs Identified and Fixes
The original functions assumed their inputs were well formed. Wrong types caused AttributeError or TypeError; member IDs with extra delimiters failed during unpacking; whitespace was retained in member types; fine CSV parsing accepted empty and negative fields inconsistently and leaked integer conversion errors; and short titles caused IndexError.

The fixed functions validate types and formats before processing. They reject missing or extra fields, negative or non-ASCII numeric values, empty CSV entries, and titles with fewer than two words. Numeric parsing handles very long ASCII values without relying on Python's string-to-integer digit limit. All invalid values follow the same documented ValueError strategy.

Installation
Python 3.8 or newer is required.

python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
On macOS or Linux, activate the environment with source .venv/bin/activate instead.

Run the Application
python library_fines.py
Example inputs are STU-1023, 10,20,30, and The Hobbit. The application prints a validation message and continues to the next prompt when an input is invalid.

Run the Fuzz Tests
python -m pytest -v test_library_fines.py
The suite checks generated valid values against reference behavior and requires malformed strings and unexpected types to raise ValueError. Each Hypothesis property test explores up to 120 examples per run. The strategies include text, integers, None, booleans, lists, and combined strategies.

Final Results
The completed suite contains 9 pytest test cases, including 6 Hypothesis properties. The final run passed all 9 tests. The initial run against the original implementation had 5 failures and 4 passes, exposing the validation bugs described above.

Deliverables
FUZZ_TESTING_REPORT.md documents the initial findings, strategies, fixes, and final run.
Lab_7_Fuzz_Testing_Report_24AM426.pdf presents the four terminal screenshots in order with explanations.
screenshots/ contains the original run, initial failures, fixed run, and final test results.
