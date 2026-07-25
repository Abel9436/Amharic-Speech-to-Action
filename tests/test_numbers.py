import pytest

from src.numbers import (
    geez_to_int,
    int_to_geez,
    is_number_token,
    replace_geez_numerals,
    words_to_int,
)


@pytest.mark.parametrize(
    ("geez", "value"),
    [
        ("፩", 1), ("፱", 9), ("፲", 10), ("፲፪", 12), ("፺፱", 99), ("፻", 100),
        ("፻፩", 101), ("፪፻", 200), ("፲፪፻፴፬", 1234), ("፳፻፲፯", 2017),
        ("፼", 10_000), ("፼፻", 10_100), ("፻፼", 1_000_000), ("፻፩፼", 1_010_000),
    ],
)  # fmt: skip
def test_geez_to_int(geez: str, value: int) -> None:
    assert geez_to_int(geez) == value
    assert int_to_geez(value) == geez


def test_roundtrip_range() -> None:
    for n in [*range(1, 20_001), 99_999_999, 12_345_678]:
        assert geez_to_int(int_to_geez(n)) == n


@pytest.mark.parametrize("bad", ["", "a", "፲x"])
def test_geez_to_int_rejects(bad: str) -> None:
    with pytest.raises(ValueError):
        geez_to_int(bad)


@pytest.mark.parametrize("bad", [0, -1, 10**8])
def test_int_to_geez_range(bad: int) -> None:
    with pytest.raises(ValueError):
        int_to_geez(bad)


def test_replace_in_sentence() -> None:
    assert replace_geez_numerals("በ፳፻፲፯ ዓ.ም ፲፪ ሰዓት") == "በ2017 ዓ.ም 12 ሰዓት"


@pytest.mark.parametrize(
    ("words", "value"),
    [
        ("አምስት", 5), ("አስራ አምስት", 15), ("ሃያ ሁለት", 22), ("ሁለት መቶ ሃምሳ", 250),
        ("መቶ", 100), ("ሦስት ሺህ አምስት መቶ", 3500), ("አሥር ሺ", 10_000),
        ("አንድ ሚሊዮን", 1_000_000),
    ],
)  # fmt: skip
def test_words_to_int(words: str, value: int) -> None:
    assert words_to_int(words) == value


@pytest.mark.parametrize("text", ["", "ሰላም", "አምስት ብር"])
def test_words_to_int_non_numbers(text: str) -> None:
    assert words_to_int(text) is None


@pytest.mark.parametrize(
    ("tok", "expected"),
    [("12", True), ("፲፪", True), ("3ኛ", True), ("ሦስት", True), ("ሰላም", False), ("", False)],
)
def test_is_number_token(tok: str, expected: bool) -> None:
    assert is_number_token(tok) is expected
