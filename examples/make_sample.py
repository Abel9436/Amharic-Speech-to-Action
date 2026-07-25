"""Run the real scoring and error-analysis code on hand-written example pairs.

The pairs in ``sample_utterances.csv`` were written by hand to show each error
bucket. They are NOT model output and NOT benchmark results.

    python -m examples.make_sample
"""

from __future__ import annotations

import csv
from pathlib import Path

from src.baseline import SUMMARY_FIELDS, UTT_FIELDS, score_utterances, summarize, write_csv
from src.eval.error_analysis import analyze, to_markdown

HERE = Path(__file__).parent


def main() -> None:
    with (HERE / "sample_utterances.csv").open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    scored = score_utterances(rows)
    write_csv(HERE / "output" / "sample_per_utterance.csv", scored, UTT_FIELDS)
    summary = summarize("EXAMPLE (hand-written pairs)", "example", scored, elapsed=0.0, seed=42)
    write_csv(HERE / "output" / "sample_summary.csv", [summary], SUMMARY_FIELDS)
    md = "> Illustrative only: hand-written pairs, not model output.\n\n"
    md += to_markdown("sample", analyze(rows))
    (HERE / "output" / "sample_errors.md").write_text(md, encoding="utf-8")
    print(f"wrote {HERE / 'output'}")


if __name__ == "__main__":
    main()
