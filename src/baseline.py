"""Zero-shot ASR baseline on FLEURS Amharic.

Writes per-utterance results to ``results/baseline/<model>_<split>.csv`` and a
summary row per model to ``results/baseline.csv``.

Example (Kaggle T4):
    python -m src.baseline --config configs/baseline.yaml --model openai/whisper-small
"""

from __future__ import annotations

import argparse
import csv
import random
import time
from pathlib import Path
from typing import Any

import yaml

from src.eval.metrics import char_counts, corpus_cer, corpus_wer, word_counts
from src.normalize import basic_clean, normalize

SUMMARY_FIELDS = [
    "model", "split", "n", "wer_raw", "wer_raw_ci_low", "wer_raw_ci_high",
    "wer_norm", "wer_norm_ci_low", "wer_norm_ci_high", "cer_norm",
    "cer_norm_ci_low", "cer_norm_ci_high", "audio_hours", "rtf",
]  # fmt: skip
UTT_FIELDS = ["id", "ref", "hyp", "wer", "cer", "wer_norm", "cer_norm", "duration"]


def model_slug(model_id: str) -> str:
    """Filesystem-safe name for a model ID."""
    return model_id.replace("/", "__")


def score_utterances(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Add raw and normalized per-utterance WER/CER to rows with ``ref``/``hyp``."""
    out = []
    for r in rows:
        ref_raw, hyp_raw = basic_clean(r["ref"]), basic_clean(r["hyp"])
        ref_n, hyp_n = normalize(r["ref"]), normalize(r["hyp"])
        out.append(
            {
                **r,
                "wer": round(word_counts(ref_raw, hyp_raw).rate, 4),
                "cer": round(char_counts(ref_raw, hyp_raw).rate, 4),
                "wer_norm": round(word_counts(ref_n, hyp_n).rate, 4),
                "cer_norm": round(char_counts(ref_n, hyp_n).rate, 4),
            }
        )
    return out


def summarize(
    model_id: str, split: str, rows: list[dict[str, Any]], elapsed: float, seed: int
) -> dict[str, Any]:
    """Corpus metrics with bootstrap CIs for one model/split."""
    refs = [r["ref"] for r in rows]
    hyps = [r["hyp"] for r in rows]
    raw = corpus_wer([basic_clean(x) for x in refs], [basic_clean(x) for x in hyps], seed=seed)
    norm = corpus_wer([normalize(x) for x in refs], [normalize(x) for x in hyps], seed=seed)
    cer_n = corpus_cer([normalize(x) for x in refs], [normalize(x) for x in hyps], seed=seed)
    audio_s = sum(float(r["duration"]) for r in rows)
    return {
        "model": model_id, "split": split, "n": len(rows),
        "wer_raw": round(raw.value, 4), "wer_raw_ci_low": round(raw.ci_low, 4),
        "wer_raw_ci_high": round(raw.ci_high, 4),
        "wer_norm": round(norm.value, 4), "wer_norm_ci_low": round(norm.ci_low, 4),
        "wer_norm_ci_high": round(norm.ci_high, 4),
        "cer_norm": round(cer_n.value, 4), "cer_norm_ci_low": round(cer_n.ci_low, 4),
        "cer_norm_ci_high": round(cer_n.ci_high, 4),
        "audio_hours": round(audio_s / 3600, 3),
        "rtf": round(elapsed / audio_s, 4) if audio_s else None,
    }  # fmt: skip


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    """Write rows to CSV (UTF-8), creating parent directories."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def upsert_summary(path: Path, row: dict[str, Any]) -> None:
    """Replace (model, split) row in the summary CSV, or append it."""
    rows: list[dict[str, Any]] = []
    if path.exists():
        with path.open(encoding="utf-8") as f:
            rows = [
                r for r in csv.DictReader(f)
                if (r["model"], r["split"]) != (row["model"], row["split"])
            ]  # fmt: skip
    rows.append(row)
    write_csv(path, rows, SUMMARY_FIELDS)


def run_model(model_cfg: dict[str, Any], cfg: dict[str, Any], args: argparse.Namespace) -> None:
    """Transcribe the split with one model and write its results."""
    from datasets import load_dataset

    from src.transcribe import ASRModel

    ds_cfg = cfg["dataset"]
    ds = load_dataset(ds_cfg["name"], ds_cfg["config"], split=args.split, trust_remote_code=True)
    ds = ds.sort("id")  # deterministic order regardless of download sharding
    if args.max_samples:
        idx = sorted(random.Random(args.seed).sample(range(len(ds)), args.max_samples))
        ds = ds.select(idx)

    asr = ASRModel(
        model_cfg["id"],
        model_cfg["family"],
        target_lang=model_cfg.get("target_lang", "amh"),
        generation=cfg.get("generation", {}) if model_cfg["family"] == "whisper" else {},
    )
    rows: list[dict[str, Any]] = []
    start = time.perf_counter()
    for i in range(0, len(ds), args.batch_size):
        batch = ds[i : i + args.batch_size]
        audios = [a["array"] for a in batch["audio"]]
        hyps = asr.transcribe(audios)
        for uid, ref, audio, hyp in zip(
            batch["id"], batch["raw_transcription"], batch["audio"], hyps, strict=True
        ):
            dur = len(audio["array"]) / audio["sampling_rate"]
            rows.append({"id": uid, "ref": ref, "hyp": hyp.strip(), "duration": round(dur, 3)})
        print(f"[{model_cfg['id']}] {len(rows)}/{len(ds)}", flush=True)
    elapsed = time.perf_counter() - start

    rows = score_utterances(rows)
    out_dir = Path(args.output_dir)
    write_csv(out_dir / "baseline" / f"{model_slug(model_cfg['id'])}_{args.split}.csv", rows,
              UTT_FIELDS)  # fmt: skip
    summary = summarize(model_cfg["id"], args.split, rows, elapsed, args.seed)
    upsert_summary(out_dir / "baseline.csv", summary)
    print(summary)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--config", default="configs/baseline.yaml")
    p.add_argument("--model", action="append", help="model ID(s) from the config; default all")
    p.add_argument("--split", default=None, help="dataset split (default from config)")
    p.add_argument("--max-samples", type=int, default=None)
    p.add_argument("--batch-size", type=int, default=None)
    p.add_argument("--output-dir", default=None)
    p.add_argument("--seed", type=int, default=None)
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    cfg = yaml.safe_load(Path(args.config).read_text(encoding="utf-8"))
    args.split = args.split or cfg["dataset"].get("split", "test")
    args.max_samples = args.max_samples or cfg["dataset"].get("max_samples")
    args.batch_size = args.batch_size or cfg.get("batch_size", 8)
    args.output_dir = args.output_dir or cfg.get("output_dir", "results")
    args.seed = cfg.get("seed", 42) if args.seed is None else args.seed
    random.seed(args.seed)

    models = cfg["models"]
    if args.model:
        known = {m["id"] for m in models}
        unknown = set(args.model) - known
        if unknown:
            raise SystemExit(f"models not in config: {sorted(unknown)}")
        models = [m for m in models if m["id"] in args.model]
    for m in models:
        run_model(m, cfg, args)


if __name__ == "__main__":
    main()
