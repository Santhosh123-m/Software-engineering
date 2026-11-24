"""Input validation helpers for the library fines lab.

Invalid values, including values of the wrong type, consistently raise
``ValueError`` with a message describing the expected format.
"""


def _parse_ascii_nonnegative_integer(value, description):
    """Parse an ASCII decimal integer without Python's string digit limit."""
    if not value or not value.isascii() or not value.isdecimal():
        raise ValueError(f"{description} must contain only non-negative ASCII digits.")

    result = 0
    for character in value:
        result = result * 10 + (ord(character) - ord("0"))
    return result


def parse_member_id(member_id):
    """Return (uppercase member type, numeric ID) for a value like ``STU-1023``."""
    if not isinstance(member_id, str):
        raise ValueError("Member ID must be a string in the format TYPE-number.")

    value = member_id.strip()
    if value.count("-") != 1:
        raise ValueError("Member ID must contain exactly one hyphen.")

    member_type, number = value.split("-")
    if not member_type.isascii() or not member_type.isalpha():
        raise ValueError("Member type must contain one or more ASCII letters.")

    member_number = _parse_ascii_nonnegative_integer(number, "Member number")
    return member_type.upper(), member_number


def total_fine(days_csv):
    """Return the total fine: 2 per day beyond 14 for each CSV day value."""
    if not isinstance(days_csv, str):
        raise ValueError("Days must be supplied as a comma-separated string.")

    value = days_csv.strip()
    if not value:
        raise ValueError("Days CSV must contain at least one integer value.")

    fine = 0
    for index, token in enumerate(value.split(","), start=1):
        day_text = token.strip()
        if not day_text:
            raise ValueError(f"Days CSV field {index} is empty.")
        days_kept = _parse_ascii_nonnegative_integer(day_text, f"Days CSV field {index}")
        if days_kept > 14:
            fine += (days_kept - 14) * 2
    return fine


def shelf_code(title):
    """Return the uppercase initials of the first two words in a book title."""
    if not isinstance(title, str):
        raise ValueError("Title must be a string containing at least two words.")

    words = title.split()
    if len(words) < 2:
        raise ValueError("Title must contain at least two whitespace-separated words.")
    return (words[0][0] + words[1][0]).upper()


def main():
    print("==== Running parse_member_id ====")
    user_input = input("Enter a member ID (e.g. STU-1023): ")
    try:
        result = parse_member_id(user_input)
        print("Member Type and Number:", result)
    except ValueError as error:
        print("Invalid member ID:", error)

    print("\n==== Running total_fine ====")
    user_input = input("Enter days kept for each book as CSV (e.g. 10,20,30): ")
    try:
        result = total_fine(user_input)
        print("Total Fine:", result)
    except ValueError as error:
        print("Invalid days CSV:", error)

    print("\n==== Running shelf_code ====")
    user_input = input("Enter a book title with at least two words: ")
    try:
        result = shelf_code(user_input)
        print("Shelf Code:", result)
    except ValueError as error:
        print("Invalid title:", error)


if __name__ == "__main__":
    main()
