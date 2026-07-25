"""Bucket ASR errors into interpretable categories.

Each contiguous non-matching alignment region between the cleaned reference
and hypothesis is assigned to exactly one bucket, checked in this order:

1. ``split_merge``   same characters, different word boundaries (ቤት ውስጥ / ቤትውስጥ)
2. ``homophone``     same words after homophone normalization (ሰዓት / ሠዓት)
3. ``number``        a digit, Ge'ez numeral or number word is involved
4. ``code_switched`` a Latin-script word is involved
5. ``deletion``      reference words with no hypothesis words
6. ``insertion``     hypothesis words with no reference words
7. ``substitution``  everything else

Utterances whose hypothesis contains a repetition loop (a 1-4 word n-gram
repeated 3+ times in a row) are additionally flagged as ``hallucination_loop``.

Example:
    python -m src.eval.error_analysis --input-dir results/baseline \
        --output results/baseline_errors.md
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

import jiwer

from src.normalize import basic_clean, normalize_chars
from src.numbers import is_number_token

BUCKETS = [
    "split_merge", "homophone", "number", "code_switched",
    "deletion", "insertion", "substitution",
]  # fmt: skip
_LATIN_RE = re.compile(r"[a-z]")


@dataclass(frozen=True)
class ErrorRegion:
    """One contiguous mismatch between reference and hypothesis words."""

    bucket: str
    ref: tuple[str, ...]
    hyp: tuple[str, ...]


def error_regions(ref_words: list[str], hyp_words: list[str]) -> list[tuple[list[str], list[str]]]:
    """Return (ref_segment, hyp_segment) for each merged run of non-equal alignment chunks."""
    if not ref_words and not hyp_words:
        return []
    if not ref_words:
        return [([], hyp_words)]
    if not hyp_words:
        return [(ref_words, [])]
    chunks = jiwer.process_words(" ".join(ref_words), " ".join(hyp_words)).alignments[0]
    regions: list[tuple[list[str], list[str]]] = []
    current: list[tuple[int, int, int, int]] = []
    for ch in [*chunks, None]:
        if ch is not None and ch.type != "equal":
            current.append((ch.ref_start_idx, ch.ref_end_idx, ch.hyp_start_idx, ch.hyp_end_idx))
            continue
        if current:
            r0, r1 = current[0][0], current[-1][1]
            h0, h1 = current[0][2], current[-1][3]
            regions.append((ref_words[r0:r1], hyp_words[h0:h1]))
            current = []
    return regions


def peel_homophones(
    ref_seg: list[str], hyp_seg: list[str]
) -> list[tuple[list[str], list[str]]]:
    """Split homophone-equal word pairs off both ends of a merged region.

    Adjacent alignment chunks are merged so split/merge errors stay whole, but that
    can also glue a homophone substitution onto a neighbouring error.
    """
    head: list[tuple[list[str], list[str]]] = []
    tail: list[tuple[list[str], list[str]]] = []
    r, h = list(ref_seg), list(hyp_seg)
    while r and h and len(r) + len(h) > 2 and normalize_chars(r[0]) == normalize_chars(h[0]):
        head.append(([r.pop(0)], [h.pop(0)]))
    while r and h and len(r) + len(h) > 2 and normalize_chars(r[-1]) == normalize_chars(h[-1]):
        tail.insert(0, ([r.pop()], [h.pop()]))
    middle = [(r, h)] if r or h else []
    return head + middle + tail


def classify_region(ref_seg: list[str], hyp_seg: list[str]) -> str:
    """Assign a single bucket to a mismatch region (see module docstring for order)."""
    ref_n = [normalize_chars(w) for w in ref_seg]
    hyp_n = [normalize_chars(w) for w in hyp_seg]
    if ref_seg and hyp_seg and len(ref_seg) != len(hyp_seg) and "".join(ref_n) == "".join(hyp_n):
        return "split_merge"
    if ref_seg and len(ref_seg) == len(hyp_seg) and ref_n == hyp_n:
        return "homophone"
    words = ref_seg + hyp_seg
    if any(is_number_token(w) for w in words):
        return "number"
    if any(_LATIN_RE.search(w) for w in words):
        return "code_switched"
    if not hyp_seg:
        return "deletion"
    if not ref_seg:
        return "insertion"
    return "substitution"


def has_repetition_loop(words: list[str], min_repeats: int = 3, max_n: int = 4) -> bool:
    """True if some n-gram (n <= max_n) repeats ``min_repeats`` times consecutively."""
    for n in range(1, max_n + 1):
        for start in range(len(words) - n * min_repeats + 1):
            gram = words[start : start + n]
            if all(
                words[start + k * n : start + (k + 1) * n] == gram for k in range(1, min_repeats)
            ):
                return True
    return False


def analyze(rows: list[dict[str, str]], max_examples: int = 10) -> dict:
    """Count error regions and word errors per bucket, collecting examples."""
    region_counts: Counter[str] = Counter()
    word_counts: Counter[str] = Counter()
    examples: dict[str, list[dict[str, str]]] = defaultdict(list)
    loops: list[dict[str, str]] = []
    for row in rows:
        ref_words = basic_clean(row["ref"]).split()
        hyp_words = basic_clean(row["hyp"]).split()
        if has_repetition_loop(hyp_words):
            loops.append({"id": row.get("id", ""), "ref": row["ref"], "hyp": row["hyp"]})
        regions = [
            part
            for region in error_regions(ref_words, hyp_words)
            for part in peel_homophones(*region)
        ]
        for ref_seg, hyp_seg in regions:
            bucket = classify_region(ref_seg, hyp_seg)
            region_counts[bucket] += 1
            word_counts[bucket] += max(len(ref_seg), len(hyp_seg))
            if len(examples[bucket]) < max_examples:
                examples[bucket].append(
                    {"id": row.get("id", ""), "ref": " ".join(ref_seg), "hyp": " ".join(hyp_seg)}
                )
    return {
        "n_utterances": len(rows),
        "regions": {b: region_counts[b] for b in BUCKETS},
        "words": {b: word_counts[b] for b in BUCKETS},
        "hallucination_loops": len(loops),
        "examples": {b: examples[b] for b in BUCKETS},
        "loop_examples": loops[:max_examples],
    }


def to_markdown(name: str, result: dict) -> str:
    """Render one model's analysis as a Markdown section."""
    total = sum(result["regions"].values()) or 1
    lines = [
        f"## {name}",
        "",
        f"Utterances: {result['n_utterances']} · "
        f"utterances with repetition loops: {result['hallucination_loops']}",
        "",
        "| bucket | regions | % regions | words affected |",
        "|---|---:|---:|---:|",
    ]
    for b in BUCKETS:
        c = result["regions"][b]
        lines.append(f"| {b} | {c} | {100 * c / total:.1f} | {result['words'][b]} |")
    for b in BUCKETS:
        if not result["examples"][b]:
            continue
        lines += ["", f"### {b} examples", "", "| id | ref | hyp |", "|---|---|---|"]
        lines += [f"| {e['id']} | {e['ref']} | {e['hyp']} |" for e in result["examples"][b]]
    if result["loop_examples"]:
        lines += ["", "### repetition-loop examples", "", "| id | hyp |", "|---|---|"]
        lines += [f"| {e['id']} | {e['hyp'][:200]} |" for e in result["loop_examples"]]
    return "\n".join(lines) + "\n"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(description="Bucket ASR errors from per-utterance CSVs.")
    p.add_argument("--input-dir", default="results/baseline")
    p.add_argument("--output", default="results/baseline_errors.md")
    p.add_argument("--max-examples", type=int, default=10)
    args = p.parse_args(argv)

    files = sorted(Path(args.input_dir).glob("*.csv"))
    if not files:
        raise SystemExit(f"no per-utterance CSVs in {args.input_dir}; run `make baseline` first")
    sections = ["# Baseline error analysis", "", "Generated by `src/eval/error_analysis.py`.", ""]
    summary = {}
    for f in files:
        result = analyze(read_rows(f), args.max_examples)
        summary[f.stem] = {k: result[k] for k in ("n_utterances", "regions", "words",
                                                    "hallucination_loops")}  # fmt: skip
        sections.append(to_markdown(f.stem, result))
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(sections), encoding="utf-8")
    out.with_suffix(".json").write_text(json.dumps(summary, ensure_ascii=False, indent=2),
                                        encoding="utf-8")  # fmt: skip
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
