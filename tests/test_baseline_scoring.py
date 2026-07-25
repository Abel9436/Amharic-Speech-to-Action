from pathlib import Path

from src.baseline import model_slug, score_utterances, summarize, upsert_summary
from src.report_tables import baseline_table, replace_block


def test_score_utterances_raw_vs_norm() -> None:
    rows = score_utterances([{"id": "a", "ref": "ሠላም ነህ።", "hyp": "ሰላም ነህ", "duration": 1.0}])
    assert rows[0]["wer"] == 0.5  # raw: homophone counted as error
    assert rows[0]["wer_norm"] == 0.0


def test_summary_and_upsert(tmp_path: Path) -> None:
    rows = score_utterances([{"id": "a", "ref": "ሰላም", "hyp": "ሰላም", "duration": 2.0}])
    s = summarize("m/x", "test", rows, elapsed=1.0, seed=0)
    path = tmp_path / "baseline.csv"
    upsert_summary(path, s)
    upsert_summary(path, s)
    assert path.read_text(encoding="utf-8").count("m/x") == 1
    assert "| `m/x` | test | 1 |" in baseline_table(path)


def test_replace_block() -> None:
    text = "x\n<!-- BEGIN:t -->\nold\n<!-- END:t -->\ny"
    assert replace_block(text, "t", "new") == "x\n<!-- BEGIN:t -->\nnew\n<!-- END:t -->\ny"


def test_model_slug() -> None:
    assert model_slug("openai/whisper-small") == "openai__whisper-small"
