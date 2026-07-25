"""Amharic text normalization for ASR training targets and evaluation.

Amharic orthography has several homophone letter families that are
pronounced identically but spelled differently (ሀ/ሐ/ኀ, ሰ/ሠ, አ/ዐ, ጸ/ፀ).
Scoring raw text penalizes an ASR model for spelling choices no listener can
hear, so we map every family to one canonical row, vowel order by vowel order.
"""

from __future__ import annotations

import re
import unicodedata

from src.numbers import replace_geez_numerals


def _row_map(src_base: int, dst_base: int, orders: int = 8) -> dict[str, str]:
    return {chr(src_base + i): chr(dst_base + i) for i in range(orders)}


# Canonical rows: ሀ (U+1200), ሰ (U+1230), አ (U+12A0), ጸ (U+1338).
HOMOPHONE_MAP: dict[str, str] = {
    **_row_map(0x1210, 0x1200, 7),  # ሐ ሑ ሒ ሓ ሔ ሕ ሖ -> ሀ ሁ ሂ ሃ ሄ ህ ሆ
    **_row_map(0x1280, 0x1200, 7),  # ኀ ኁ ኂ ኃ ኄ ኅ ኆ -> ሀ ...
    **_row_map(0x1220, 0x1230, 8),  # ሠ ... ሧ -> ሰ ... ሷ
    **_row_map(0x12D0, 0x12A0, 7),  # ዐ ዑ ዒ ዓ ዔ ዕ ዖ -> አ ...
    **_row_map(0x1340, 0x1338, 8),  # ፀ ... ፇ -> ጸ ... ጿ
    "ሗ": "ኋ",  # ሗ -> ኋ (both "hwa")
}
# The 4th order (ሃ) of the ሀ row is pronounced like the 1st (ሀ); same for አ/ኣ.
HOMOPHONE_MAP.update({"ሃ": "ሀ", "ኣ": "አ"})
# Apply the vowel-order collapse after family mapping too (ሓ -> ሃ -> ሀ).
HOMOPHONE_MAP = {k: HOMOPHONE_MAP.get(v, v) for k, v in HOMOPHONE_MAP.items()}

# Labialized "-wa" glyphs are often written as Cu + ዋ (ኋላ / ሁዋላ).
# We decompose to the two-glyph spelling so both forms compare equal.
_LABIAL_PAIRS = {
    "ሏ": "ሉ", "ሟ": "ሙ", "ሯ": "ሩ", "ሷ": "ሱ", "ሿ": "ሹ", "ቧ": "ቡ", "ቷ": "ቱ",
    "ቿ": "ቹ", "ኗ": "ኑ", "ኟ": "ኙ", "ዟ": "ዙ", "ዧ": "ዡ", "ዷ": "ዱ", "ጇ": "ጁ",
    "ጧ": "ጡ", "ጯ": "ጩ", "ጷ": "ጱ", "ጿ": "ጹ", "ፏ": "ፉ", "ቋ": "ቁ", "ኳ": "ኩ",
    "ጓ": "ጉ", "ኋ": "ሁ",
}  # fmt: skip
LABIALIZED_MAP: dict[str, str] = {k: v + "ዋ" for k, v in _LABIAL_PAIRS.items()}

# Ethiopic punctuation; ፡ (word space) becomes a space, the rest are dropped.
ETHIOPIC_PUNCT = "።፣፤፥፦፧፨፠"
_PUNCT_RE = re.compile(rf"[{ETHIOPIC_PUNCT}\"'`“”‘’«»!?.,;:()\[\]{{}}<>/\\|@#$%^&*_+=~-]")
_WS_RE = re.compile(r"\s+")


def normalize_chars(text: str, *, labialized: bool = False) -> str:
    """Apply only the letter-level homophone (and optional labial) mapping."""
    text = "".join(HOMOPHONE_MAP.get(ch, ch) for ch in text)
    if labialized:
        text = "".join(LABIALIZED_MAP.get(ch, ch) for ch in text)
    return text


def basic_clean(text: str) -> str:
    """Light cleanup used for "raw" WER: NFC, lowercase, strip punctuation, collapse spaces.

    Spelling (homophones, numerals) is left untouched.
    """
    text = unicodedata.normalize("NFC", text or "")
    text = text.replace("፡", " ").lower()
    text = _PUNCT_RE.sub(" ", text)
    return _WS_RE.sub(" ", text).strip()


def normalize(
    text: str,
    *,
    homophones: bool = True,
    labialized: bool = False,
    geez_numerals: bool = True,
) -> str:
    """Full normalization for training targets and "normalized" WER.

    Args:
        text: input string (may mix Ethiopic, Latin and digits).
        homophones: collapse homophone letter families to one canonical row.
        labialized: decompose labialized -wa glyphs (ኋ -> ሁዋ).
        geez_numerals: convert Ge'ez numerals (፲፪) to Arabic digits (12).
    """
    text = unicodedata.normalize("NFC", text or "")
    if geez_numerals:
        text = replace_geez_numerals(text)
    if homophones:
        text = normalize_chars(text, labialized=labialized)
    elif labialized:
        text = "".join(LABIALIZED_MAP.get(ch, ch) for ch in text)
    return basic_clean(text)
