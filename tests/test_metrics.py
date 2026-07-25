import pytest

from src.eval.metrics import (
    EditCounts,
    bootstrap_ci,
    cer,
    corpus_cer,
    corpus_rate,
    corpus_wer,
    wer,
    word_counts,
)


def test_wer_perfect_and_counts() -> None:
    assert wer("ሰላም ነህ", "ሰላም ነህ") == 0.0
    c = word_counts("a b c", "a x c d")
    assert (c.substitutions, c.deletions, c.insertions, c.ref_len) == (1, 0, 1, 3)


def test_wer_empty_cases() -> None:
    assert wer("", "") == 0.0
    assert wer("", "ሰላም") == 1.0
    assert wer("ሰላም ነህ", "") == 1.0


def test_cer_ignores_spaces() -> None:
    assert cer("ቤት ውስጥ", "ቤትውስጥ") == 0.0
    assert cer("abcd", "abxd") == pytest.approx(0.25)


def test_corpus_rate_is_weighted_not_mean() -> None:
    counts = [EditCounts(1, 0, 0, 1), EditCounts(0, 0, 0, 9)]
    assert corpus_rate(counts) == pytest.approx(0.1)


def test_corpus_wer_with_ci() -> None:
    refs = ["a b c d"] * 20 + ["a b"] * 20
    hyps = ["a b c d"] * 20 + ["a x"] * 20
    score = corpus_wer(refs, hyps, n_resamples=200)
    assert score.value == pytest.approx(20 / 120)
    assert score.ci_low <= score.value <= score.ci_high


def test_bootstrap_deterministic() -> None:
    counts = [EditCounts(i % 3, 0, 0, 5) for i in range(30)]
    assert bootstrap_ci(counts, seed=1) == bootstrap_ci(counts, seed=1)


def test_corpus_cer_length_mismatch_raises() -> None:
    with pytest.raises(ValueError):
        corpus_cer(["a"], ["a", "b"])
