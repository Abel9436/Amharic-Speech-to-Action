"""Ge'ez (Ethiopic) numerals and Amharic number words <-> integers.

Ge'ez numerals have no zero and no place value. Values are written as pairs
of (tens, ones) glyphs joined by the multipliers ፻ (100) and ፼ (10,000).
Examples: ፲፪ = 12, ፻ = 100, ፲፪፻፴፬ = 1234, ፼ = 10,000, ፻፼ = 1,000,000.
"""

from __future__ import annotations

import re

GEEZ_ONES = {chr(0x1369 + i): i + 1 for i in range(9)}  # ፩..፱
GEEZ_TENS = {chr(0x1372 + i): (i + 1) * 10 for i in range(9)}  # ፲..፺
GEEZ_HUNDRED = "፻"  # ፻
GEEZ_TEN_THOUSAND = "፼"  # ፼
GEEZ_CHARS = "".join(GEEZ_ONES) + "".join(GEEZ_TENS) + GEEZ_HUNDRED + GEEZ_TEN_THOUSAND
GEEZ_RUN_RE = re.compile(f"[{GEEZ_CHARS}]+")

_ONES_BY_VALUE = {v: k for k, v in GEEZ_ONES.items()}
_TENS_BY_VALUE = {v: k for k, v in GEEZ_TENS.items()}

MAX_GEEZ = 10**8 - 1


def geez_to_int(text: str) -> int:
    """Parse a run of Ge'ez numeral characters into an integer.

    Raises:
        ValueError: if ``text`` is empty or contains non-numeral characters.
    """
    if not text:
        raise ValueError("empty Ge'ez numeral")
    total = 0  # completed ፼ groups
    group = 0  # completed ፻ part inside the current ፼ group
    pair = 0  # current 1..99 accumulator
    for ch in text:
        if ch in GEEZ_ONES:
            pair += GEEZ_ONES[ch]
        elif ch in GEEZ_TENS:
            pair += GEEZ_TENS[ch]
        elif ch == GEEZ_HUNDRED:
            group += (pair or 1) * 100
            pair = 0
        elif ch == GEEZ_TEN_THOUSAND:
            current = group + pair
            if current == 0 and total > 0:
                total *= 10_000  # ፼፼ = 10^8
            else:
                total += (current or 1) * 10_000
            group = pair = 0
        else:
            raise ValueError(f"not a Ge'ez numeral character: {ch!r}")
    return total + group + pair


def _pair_to_geez(value: int) -> str:
    tens, ones = divmod(value, 10)
    return _TENS_BY_VALUE.get(tens * 10, "") + _ONES_BY_VALUE.get(ones, "")


def int_to_geez(n: int) -> str:
    """Render a positive integer (< 10^8) in Ge'ez numerals."""
    if not 1 <= n <= MAX_GEEZ:
        raise ValueError(f"Ge'ez conversion supports 1..{MAX_GEEZ}, got {n}")
    digits = str(n)
    if len(digits) % 2:
        digits = "0" + digits
    pairs = [int(digits[i : i + 2]) for i in range(0, len(digits), 2)]
    out = []
    top = len(pairs) - 1
    for idx, value in enumerate(pairs):
        k = top - idx  # pair position from the right
        if k == 0:
            out.append(_pair_to_geez(value))
            continue
        if value:
            # A bare ፻/፼ means one hundred / ten thousand, except a non-leading ፩፼.
            omit_one = value == 1 and (idx == 0 or k % 2 == 1)
            out.append("" if omit_one else _pair_to_geez(value))
        if k % 2 == 1 and value:
            out.append(GEEZ_HUNDRED)
        elif k % 2 == 0 and (value or (idx > 0 and pairs[idx - 1])):
            out.append(GEEZ_TEN_THOUSAND)
    return "".join(out)


def replace_geez_numerals(text: str) -> str:
    """Replace every run of Ge'ez numerals in ``text`` with Arabic digits."""
    return GEEZ_RUN_RE.sub(lambda m: str(geez_to_int(m.group())), text)


# Number words in homophone-normalized spelling (see normalize.normalize_chars).
_WORD_UNITS = {
    "አንድ": 1, "ሁለት": 2, "ሶስት": 3, "አራት": 4, "አምስት": 5,
    "ስድስት": 6, "ሰባት": 7, "ስምንት": 8, "ዘጠኝ": 9, "አስር": 10,
    "አስራ": 10, "ሀያ": 20, "ሰላሳ": 30, "አርባ": 40, "ሀምሳ": 50,
    "ስልሳ": 60, "ስድሳ": 60, "ሰባ": 70, "ሰማንያ": 80, "ዘጠና": 90,
}  # fmt: skip
_WORD_SCALES = {"መቶ": 100, "ሺ": 1000, "ሺህ": 1000, "ሚሊዮን": 1_000_000}
NUMBER_WORDS = frozenset(_WORD_UNITS) | frozenset(_WORD_SCALES)


def words_to_int(text: str) -> int | None:
    """Parse a space-separated Amharic number phrase, e.g. "ሁለት መቶ ሀምሳ" -> 250.

    Homophone spellings (ሦስት, አሥር, ሃምሳ ...) are accepted. Returns ``None``
    if any token is not a number word.
    """
    from src.normalize import normalize_chars

    tokens = normalize_chars(text).split()
    if not tokens:
        return None
    total = 0
    current = 0
    for tok in tokens:
        if tok in _WORD_UNITS:
            current += _WORD_UNITS[tok]
        elif tok in _WORD_SCALES:
            scale = _WORD_SCALES[tok]
            if scale == 100:
                current = (current or 1) * 100
            else:
                total += (current or 1) * scale
                current = 0
        else:
            return None
    return total + current


def is_number_token(token: str) -> bool:
    """True if a token is digits, Ge'ez numerals, or an Amharic number word."""
    from src.normalize import normalize_chars

    if not token:
        return False
    if any(ch.isdigit() for ch in token) or GEEZ_RUN_RE.search(token):
        return True
    return normalize_chars(token) in NUMBER_WORDS
