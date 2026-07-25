"""ASR metrics: per-utterance and corpus WER/CER with bootstrap confidence intervals.

Corpus WER is total edit errors / total reference words (not the mean of
per-utterance WERs), matching how WER is reported in the ASR literature.
"""

from __future__ import annotations

import random
from collections.abc import Sequence
from dataclasses import dataclass

import jiwer


@dataclass(frozen=True)
class EditCounts:
    """Edit operations between one reference and one hypothesis."""

    substitutions: int
    deletions: int
    insertions: int
    ref_len: int

    @property
    def errors(self) -> int:
        return self.substitutions + self.deletions + self.insertions

    @property
    def rate(self) -> float:
        """Error rate; with an empty reference, any insertion counts as 100%."""
        if self.ref_len == 0:
            return 0.0 if self.errors == 0 else 1.0
        return self.errors / self.ref_len


def _counts(ref: str, hyp: str, unit: str) -> EditCounts:
    ref_units = ref.split() if unit == "word" else list(ref.replace(" ", ""))
    hyp_units = hyp.split() if unit == "word" else list(hyp.replace(" ", ""))
    if not ref_units:
        return EditCounts(0, 0, len(hyp_units), 0)
    if not hyp_units:
        return EditCounts(0, len(ref_units), 0, len(ref_units))
    out = jiwer.process_words(" ".join(ref_units), " ".join(hyp_units))
    return EditCounts(out.substitutions, out.deletions, out.insertions, len(ref_units))


def word_counts(ref: str, hyp: str) -> EditCounts:
    """Word-level edit counts (whitespace tokenization)."""
    return _counts(ref, hyp, "word")


def char_counts(ref: str, hyp: str) -> EditCounts:
    """Character-level edit counts; spaces are ignored so splits/merges cost nothing."""
    return _counts(ref, hyp, "char")


def wer(ref: str, hyp: str) -> float:
    """Per-utterance word error rate."""
    return word_counts(ref, hyp).rate


def cer(ref: str, hyp: str) -> float:
    """Per-utterance character error rate (spaces excluded)."""
    return char_counts(ref, hyp).rate


def corpus_rate(counts: Sequence[EditCounts]) -> float:
    """Corpus-level error rate: sum of errors over sum of reference lengths."""
    total_ref = sum(c.ref_len for c in counts)
    total_err = sum(c.errors for c in counts)
    if total_ref == 0:
        return 0.0 if total_err == 0 else 1.0
    return total_err / total_ref


def bootstrap_ci(
    counts: Sequence[EditCounts],
    *,
    n_resamples: int = 1000,
    alpha: float = 0.05,
    seed: int = 42,
) -> tuple[float, float]:
    """Percentile bootstrap CI for corpus error rate, resampling utterances."""
    if not counts:
        return (0.0, 0.0)
    rng = random.Random(seed)
    n = len(counts)
    stats = sorted(
        corpus_rate([counts[rng.randrange(n)] for _ in range(n)]) for _ in range(n_resamples)
    )
    lo = stats[int((alpha / 2) * n_resamples)]
    hi = stats[min(n_resamples - 1, int((1 - alpha / 2) * n_resamples))]
    return (lo, hi)


@dataclass(frozen=True)
class CorpusScore:
    """Corpus metric with its bootstrap confidence interval."""

    value: float
    ci_low: float
    ci_high: float


def corpus_wer(
    refs: Sequence[str], hyps: Sequence[str], *, n_resamples: int = 1000, seed: int = 42
) -> CorpusScore:
    """Corpus WER with a 95% bootstrap CI."""
    counts = [word_counts(r, h) for r, h in zip(refs, hyps, strict=True)]
    lo, hi = bootstrap_ci(counts, n_resamples=n_resamples, seed=seed)
    return CorpusScore(corpus_rate(counts), lo, hi)


def corpus_cer(
    refs: Sequence[str], hyps: Sequence[str], *, n_resamples: int = 1000, seed: int = 42
) -> CorpusScore:
    """Corpus CER with a 95% bootstrap CI."""
    counts = [char_counts(r, h) for r, h in zip(refs, hyps, strict=True)]
    lo, hi = bootstrap_ci(counts, n_resamples=n_resamples, seed=seed)
    return CorpusScore(corpus_rate(counts), lo, hi)
