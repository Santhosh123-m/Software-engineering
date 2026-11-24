"""Property-based tests for the library fines input functions."""

import string

import pytest
from hypothesis import given, settings, strategies as st

from library_fines import parse_member_id, shelf_code, total_fine


FUZZ_SETTINGS = settings(max_examples=120, deadline=None)


def _is_valid_member_id(value):
    value = value.strip()
    if value.count("-") != 1:
        return False
    member_type, number = value.split("-")
    return (
        member_type.isascii()
        and member_type.isalpha()
        and number.isascii()
        and number.isdecimal()
    )


def _is_valid_days_csv(value):
    if not value.strip():
        return False
    tokens = value.split(",")
    return all(
        token.strip()
        and token.strip().isascii()
        and token.strip().isdecimal()
        for token in tokens
    )


NON_STRING_VALUES = st.one_of(
    st.none(),
    st.integers(),
    st.booleans(),
    st.lists(st.text(), max_size=5),
)


@FUZZ_SETTINGS
@given(
    member_type=st.text(
        alphabet=string.ascii_letters, min_size=1, max_size=10
    ),
    number=st.integers(min_value=0, max_value=10**100),
)
def test_parse_member_id_accepts_valid_generated_ids(member_type, number):
    result = parse_member_id(f"{member_type}-{number}")
    assert result == (member_type.upper(), number)


@FUZZ_SETTINGS
@given(
    value=st.one_of(
        st.text().filter(lambda text: not _is_valid_member_id(text)),
        NON_STRING_VALUES,
    )
)
def test_parse_member_id_rejects_malformed_values(value):
    with pytest.raises(ValueError):
        parse_member_id(value)


def test_parse_member_id_accepts_outer_whitespace_and_rejects_bad_formats():
    assert parse_member_id("  stu-1023  ") == ("STU", 1023)
    for value in (
        "",
        "STU",
        "-1023",
        "STU-",
        "STU-10-23",
        "STU--23",
        "STU-abc",
        "STU--1",
        "STU-１２３",
        "学-23",
        "STU -23",
    ):
        with pytest.raises(ValueError):
            parse_member_id(value)


@FUZZ_SETTINGS
@given(days=st.lists(st.integers(min_value=0, max_value=10**60), min_size=1, max_size=20))
def test_total_fine_matches_reference_model(days):
    days_csv = ",".join(str(day) for day in days)
    expected = sum(max(day - 14, 0) * 2 for day in days)
    assert total_fine(days_csv) == expected


@FUZZ_SETTINGS
@given(
    value=st.one_of(
        st.text().filter(lambda text: not _is_valid_days_csv(text)),
        NON_STRING_VALUES,
    )
)
def test_total_fine_rejects_malformed_values(value):
    with pytest.raises(ValueError):
        total_fine(value)


def test_total_fine_handles_boundaries_and_rejects_bad_csv_fields():
    assert total_fine(" 0, 14, 15, 20 ") == 14
    for value in ("", " ", ",", "1,,2", "1,", ",1", "-1", "1.5", "ten", "１２"):
        with pytest.raises(ValueError):
            total_fine(value)


TITLE_WORD = st.text(
    alphabet=string.ascii_letters + string.digits + "#@-é雪ß",
    min_size=1,
    max_size=12,
)


@FUZZ_SETTINGS
@given(words=st.lists(TITLE_WORD, min_size=2, max_size=8))
def test_shelf_code_uses_first_two_word_initials(words):
    title = " ".join(words)
    expected = (words[0][0] + words[1][0]).upper()
    assert shelf_code(title) == expected


@FUZZ_SETTINGS
@given(
    title=st.one_of(
        st.text().filter(lambda text: len(text.split()) < 2),
        NON_STRING_VALUES,
    )
)
def test_shelf_code_rejects_titles_with_fewer_than_two_words(title):
    with pytest.raises(ValueError):
        shelf_code(title)


def test_shelf_code_handles_spacing_unicode_and_special_characters():
    assert shelf_code("  the   Hobbit  ") == "TH"
    assert shelf_code("雪 sky") == "雪S"
    assert shelf_code("3# 2nd Edition") == "32"
