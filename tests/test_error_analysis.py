import pytest

from src.eval.error_analysis import (
    analyze,
    classify_region,
    error_regions,
    has_repetition_loop,
    peel_homophones,
)


@pytest.mark.parametrize(
    ("ref", "hyp", "bucket"),
    [
        (["ቤት", "ውስጥ"], ["ቤትውስጥ"], "split_merge"),
        (["ሠዓት"], ["ሰአት"], "homophone"),
        (["አምስት"], ["5"], "number"),
        (["ዋይፋይ"], ["wifi"], "code_switched"),
        (["ነገ"], [], "deletion"),
        ([], ["እና"], "insertion"),
        (["ቤት"], ["ቦታ"], "substitution"),
    ],
)
def test_classify_region(ref: list[str], hyp: list[str], bucket: str) -> None:
    assert classify_region(ref, hyp) == bucket


def test_error_regions_merges_adjacent_chunks() -> None:
    regions = error_regions(["እኔ", "ቤት", "ውስጥ", "ነኝ"], ["እኔ", "ቤትውስጥ", "ነኝ"])
    assert regions == [(["ቤት", "ውስጥ"], ["ቤትውስጥ"])]


def test_peel_homophones_keeps_split_merge_intact() -> None:
    assert peel_homophones(["ሠዓት", "ቤት", "ውስጥ"], ["ሰዓት", "ቤትውስጥ"]) == [
        (["ሠዓት"], ["ሰዓት"]),
        (["ቤት", "ውስጥ"], ["ቤትውስጥ"]),
    ]


def test_repetition_loop() -> None:
    assert has_repetition_loop("እና እና እና".split())
    assert has_repetition_loop("ሰላም ነህ ሰላም ነህ ሰላም ነህ".split())
    assert not has_repetition_loop("ሰላም ነህ ደህና".split())


def test_analyze_counts() -> None:
    rows = [
        {"id": "1", "ref": "ሠዓት ቤት ውስጥ", "hyp": "ሰዓት ቤትውስጥ"},
        {"id": "2", "ref": "ነገ", "hyp": "ነገ እና እና እና"},
    ]
    result = analyze(rows)
    assert result["regions"]["homophone"] == 1
    assert result["regions"]["split_merge"] == 1
    assert result["regions"]["insertion"] == 1
    assert result["hallucination_loops"] == 1
