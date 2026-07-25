import pytest

from src.normalize import basic_clean, normalize, normalize_chars


@pytest.mark.parametrize(
    ("a", "b"),
    [
        ("ሐሙስ", "ሀሙስ"),  # ሐ family
        ("ኀይል", "ሀይል"),  # ኀ family
        ("ሠላም", "ሰላም"),  # ሠ family
        ("ዐይን", "አይን"),  # ዐ family
        ("ፀሐይ", "ጸሀይ"),  # ፀ family + ሐ
        ("ሥራ", "ስራ"),  # 6th order of ሠ row
        ("ሦስት", "ሶስት"),  # 7th order
        ("ሃያ", "ሀያ"),  # ሃ pronounced like ሀ
    ],
)
def test_homophone_families_collapse(a: str, b: str) -> None:
    assert normalize(a) == normalize(b)


def test_vowel_order_is_preserved() -> None:
    # Only the family is collapsed; ሑ/ሒ keep their vowel.
    assert normalize_chars("ሑሒሔሕሖ") == "ሁሂሄህሆ"


def test_homophones_can_be_disabled() -> None:
    assert normalize("ሠላም", homophones=False) == "ሠላም"


def test_ethiopic_punctuation_and_word_space() -> None:
    assert normalize("ሰላም፡ነህ፣ ደህና ነኝ።") == "ሰላም ነህ ደህና ነኝ"


def test_question_mark_and_latin_punct() -> None:
    assert normalize("ምን ነው፧ really?!") == "ምን ነው really"


def test_whitespace_collapsed() -> None:
    assert normalize("  ሰላም \t\n  ዓለም  ") == "ሰላም አለም"


@pytest.mark.parametrize("text", ["", "   ", "።፣፤"])
def test_empty_and_punct_only(text: str) -> None:
    assert normalize(text) == ""


def test_none_safe() -> None:
    assert basic_clean(None) == ""  # type: ignore[arg-type]


def test_mixed_latin_ethiopic_lowercased() -> None:
    assert normalize("WiFi ሠርቷል Ethio Telecom") == "wifi ሰርቷል ethio telecom"


def test_geez_numerals_converted() -> None:
    assert normalize("፲፪ ሰዓት") == "12 ሰአት"


def test_geez_numeral_attached_to_suffix() -> None:
    assert normalize("፫ኛ") == "3ኛ"


def test_geez_numerals_can_be_kept() -> None:
    assert normalize("፲፪", geez_numerals=False) == "፲፪"


def test_arabic_digits_untouched() -> None:
    assert normalize("100 ብር") == "100 ብር"


def test_labialized_variants() -> None:
    assert normalize("ኋላ", labialized=True) == normalize("ሁዋላ", labialized=True)
    assert normalize("ሗላ", labialized=True) == normalize("ሁዋላ", labialized=True)
    assert normalize("ቋንቋ", labialized=True) == "ቁዋንቁዋ"


def test_labialized_off_by_default_but_hwa_unified() -> None:
    assert normalize("ኋላ") == normalize("ሗላ") == "ኋላ"


def test_nfc_composition() -> None:
    import unicodedata

    decomposed = unicodedata.normalize("NFD", "café")
    assert normalize(decomposed) == "café"


def test_idempotent() -> None:
    text = "ፀሐይ ፲፪ ሠዓት፣ WiFi።"
    assert normalize(normalize(text)) == normalize(text)
