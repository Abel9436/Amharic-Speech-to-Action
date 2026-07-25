"""Fill README result tables from files in ``results/`` so no number is typed by hand.

Tables live between ``<!-- BEGIN:<name> -->`` and ``<!-- END:<name> -->`` markers.

Example:
    python -m src.report_tables --readme README.md
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


def _pct(value: str) -> str:
    return f"{100 * float(value):.1f}"


def baseline_table(path: Path) -> str:
    """Markdown table from ``results/baseline.csv``."""
    if not path.exists():
        return "_No results yet: run `make baseline`._"
    with path.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    lines = [
        "| model | split | n | WER raw % (95% CI) | WER norm % (95% CI) | CER norm % (95% CI) |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for r in rows:
        cells = []
        for key in ("wer_raw", "wer_norm", "cer_norm"):
            cells.append(
                f"{_pct(r[key])} ({_pct(r[key + '_ci_low'])}–{_pct(r[key + '_ci_high'])})"
            )
        lines.append(f"| `{r['model']}` | {r['split']} | {r['n']} | " + " | ".join(cells) + " |")
    return "\n".join(lines)


def replace_block(text: str, name: str, body: str) -> str:
    """Replace the content between the named markers."""
    pattern = re.compile(rf"(<!-- BEGIN:{name} -->\n).*?(\n<!-- END:{name} -->)", re.DOTALL)
    if not pattern.search(text):
        raise ValueError(f"markers for {name!r} not found")
    return pattern.sub(lambda m: m.group(1) + body + m.group(2), text)


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--readme", default="README.md")
    p.add_argument("--results-dir", default="results")
    args = p.parse_args(argv)
    readme = Path(args.readme)
    text = readme.read_text(encoding="utf-8")
    text = replace_block(text, "baseline", baseline_table(Path(args.results_dir) / "baseline.csv"))
    readme.write_text(text, encoding="utf-8")
    print(f"updated {readme}")


if __name__ == "__main__":
    main()
