# Reflection — Static Code Analysis

### 1. What is static code analysis, and why is it important?

Static code analysis examines source code without executing it to identify potential bugs, security vulnerabilities, and coding style issues. It helps improve code quality, security, readability, and maintainability.

### 2. What issues did you identify in the program?

The original program had a potential SQL injection vulnerability caused by constructing SQL queries using f-strings. It also used `eval()`, which can execute unsafe expressions. Other issues included broad exception handling, an unused variable, long lines, missing docstrings, inconsistent function naming, and improper file handling.

### 3. How did you fix the identified issues?

I replaced the SQL f-string with a parameterized query and removed `eval()` by validating the salary expression and safely processing its numeric values. I also removed the unused variable, improved exception handling, used snake_case function names, added docstrings, corrected formatting, and used a context manager with explicit file encoding for report generation.

### 4. What did you learn from using Pylint, Bandit, and Flake8?

I learned that the tools serve different purposes. Pylint checks code quality and programming practices, Bandit identifies potential security vulnerabilities, and Flake8 detects style and formatting violations. Running the tools again after fixing the code helped verify the improvements. The Pylint score increased from 4.47/10 to 10.00/10, and Bandit reported no remaining issues.