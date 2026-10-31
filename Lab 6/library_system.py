"""Library fine and book renewal tracker for a campus library."""
import ast
import json
import operator
from datetime import datetime

# Global state
loans = {}
FINE_PER_DAY = 2


def add_book_loan(student_id, book_id, dates=None):
    """Record that a student borrowed a book."""
    if not student_id:
        print("Loan rejected: missing student id")
        return
    if not isinstance(book_id, str):
        print(f"Loan rejected: book id {book_id!r} must be a string")
        return
    if dates is None:
        dates = []
    dates.append(str(datetime.now()))
    loans[student_id] = loans.get(student_id, []) + [book_id]
    print(f"{student_id} borrowed {book_id} "
          f"(loan dates on record: {len(dates)})")


def return_book(student_id, book_id):
    """Remove a book from a student's loans, reporting unknown loans."""
    try:
        loans[student_id].remove(book_id)
        if len(loans[student_id]) == 0:
            del loans[student_id]
    except (KeyError, ValueError):
        print(f"Cannot return {book_id}: {student_id} has no such loan")


def calculate_fine(days_overdue):
    """Return the fine for the given days overdue (never negative)."""
    return max(days_overdue, 0) * FINE_PER_DAY


def renew_book(student_id, book_id, extra_days):
    """Renew a book; renewing must not change the fine rate for others."""
    print(f"Renewed {book_id} for {student_id} by {extra_days} days")


def load_records(file="loans.json"):
    """Load loan records from a JSON file into the loans dictionary."""
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    loans.clear()
    loans.update(data)


def save_records(file="loans.json"):
    """Save the loans dictionary to a JSON file."""
    with open(file, "w", encoding="utf-8") as f:
        json.dump(loans, f)


_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
}


def _safe_eval(node):
    """Evaluate a parsed arithmetic expression without using eval."""
    if isinstance(node, ast.Expression):
        return _safe_eval(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPERATORS:
        return _OPERATORS[type(node.op)](
            _safe_eval(node.left), _safe_eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPERATORS:
        return _OPERATORS[type(node.op)](_safe_eval(node.operand))
    raise ValueError("Unsupported expression in fine rule")


def fine_from_rule(rule, days):
    """Compute a fine from an arithmetic rule such as 'days * 2 + 10'."""
    # Only plain arithmetic is allowed; anything else raises ValueError
    return _safe_eval(ast.parse(rule.replace("days", str(days)), mode="eval"))


def print_report():
    """Print every student and the books they currently hold."""
    print("Loan Report")
    for student, books in loans.items():
        print(student, "->", books)


def main():
    """Run the demo scenario."""
    add_book_loan("S101", "B-ALGO")
    add_book_loan("S102", "B-NETW")
    add_book_loan("", "B-DBMS")
    add_book_loan("S103", 4521)  # book id should be a string
    return_book("S999", "B-NONE")
    renew_book("S101", "B-ALGO", 21)
    print("Fine for 5 days:", calculate_fine(5))
    print("Fine for -3 days:", calculate_fine(-3))
    print("Fine via rule:", fine_from_rule("days * 2 + 10", 4))
    days = input("Days overdue for S102 (press Enter for 0): ") or "0"
    try:
        print("S102 owes:", calculate_fine(int(days)))
    except ValueError:
        print("Invalid number of days:", days)
    save_records()
    load_records()
    print_report()


if __name__ == "__main__":
    main()
