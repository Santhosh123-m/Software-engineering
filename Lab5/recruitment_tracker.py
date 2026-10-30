
"""Applicant tracking system with SQLite storage and reporting."""

import csv
import re
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute(
    """
    CREATE TABLE applicants (
        id INTEGER PRIMARY KEY,
        name TEXT,
        role TEXT,
        expected_salary INTEGER,
        status TEXT
    )
    """
)


def add_applicant(name, role, expected_salary, status="applied"):
    """Add an applicant to the database using parameterized SQL."""
    conn.execute(
        """
        INSERT INTO applicants (name, role, expected_salary, status)
        VALUES (?, ?, ?, ?)
        """,
        (name, role, expected_salary, status),
    )
    conn.commit()


def shortlist(role, salary_rule):
    """Return applicants whose salary is within the specified limit.

    Accepts a non-negative integer or a simple addition expression,
    such as '500000 + 150000'.
    """
    if re.fullmatch(r"\s*\d+\s*(?:\+\s*\d+\s*)?", salary_rule) is None:
        raise ValueError(
            "Salary rule must be an integer or a simple addition expression."
        )

    numbers = re.findall(r"\d+", salary_rule)
    limit = sum(int(number) for number in numbers)

    rows = conn.execute(
        """
        SELECT name, expected_salary
        FROM applicants
        WHERE role = ?
        """,
        (role,),
    ).fetchall()

    result = [
        name for name, salary in rows if salary <= limit
    ]
    return result


def update_status(applicant_id, status):
    """Update an applicant's hiring status."""
    cursor = conn.execute(
        "UPDATE applicants SET status = ? WHERE id = ?",
        (status, applicant_id),
    )
    conn.commit()

    if cursor.rowcount == 0:
        raise ValueError(f"No applicant found with ID {applicant_id}.")


def export_report(path):
    """Export applicant names, roles, and statuses to a CSV file."""
    with open(path, "w", newline="", encoding="utf-8") as report_file:
        writer = csv.writer(report_file)
        writer.writerow(["name", "role", "status"])
        writer.writerows(
            conn.execute("SELECT name, role, status FROM applicants")
        )


def count_by_status(status):
    """Return the number of applicants with the specified status."""
    return conn.execute(
        "SELECT COUNT(*) FROM applicants WHERE status = ?",
        (status,),
    ).fetchone()[0]


def main():
    """Run a demonstration of the applicant tracking system."""
    add_applicant("Nina", "analyst", 600000)
    add_applicant("Omar", "analyst", 750000, "interview")
    add_applicant("Priya", "developer", 900000)

    update_status(1, "interview")

    print(shortlist("analyst", "500000 + 150000"))
    export_report("applicants_report.csv")
    print(count_by_status("interview"), "in interview")


if __name__ == "__main__":
    main()
