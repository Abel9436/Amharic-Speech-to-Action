"""Unified ASR interface for Whisper and MMS checkpoints.

Heavy dependencies (torch, transformers) are imported lazily so the rest of
the package stays importable in lightweight test environments.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any

SAMPLE_RATE = 16_000


@dataclass
class ASRModel:
    """A loaded ASR checkpoint with a batch ``transcribe`` method."""

    model_id: str
    family: str  # "whisper" | "mms"
    target_lang: str = "amh"
    generation: dict[str, Any] = field(default_factory=dict)
    device: str | None = None

    def __post_init__(self) -> None:
        import torch

        self.device = self.device or ("cuda" if torch.cuda.is_available() else "cpu")
        dtype = torch.float16 if self.device == "cuda" else torch.float32
        if self.family == "whisper":
            from transformers import WhisperForConditionalGeneration, WhisperProcessor

            self.processor = WhisperProcessor.from_pretrained(self.model_id)
            self.model = WhisperForConditionalGeneration.from_pretrained(
                self.model_id, torch_dtype=dtype
            )
        elif self.family == "mms":
            from transformers import AutoProcessor, Wav2Vec2ForCTC

            self.processor = AutoProcessor.from_pretrained(self.model_id)
            self.processor.tokenizer.set_target_lang(self.target_lang)
            self.model = Wav2Vec2ForCTC.from_pretrained(self.model_id, torch_dtype=dtype)
            self.model.load_adapter(self.target_lang)
        else:
            raise ValueError(f"unknown ASR family: {self.family}")
        self.dtype = dtype
        self.model.to(self.device).eval()

    def transcribe(self, audios: Sequence[Any]) -> list[str]:
        """Transcribe a batch of 16 kHz mono float arrays."""
        import torch

        audios = [a for a in audios]
        if self.family == "whisper":
            feats = self.processor.feature_extractor(
                audios, sampling_rate=SAMPLE_RATE, return_tensors="pt"
            ).input_features.to(self.device, self.dtype)
            gen = {"language": "amharic", "task": "transcribe", **self.generation}
            with torch.no_grad():
                ids = self.model.generate(feats, **gen)
            return self.processor.batch_decode(ids, skip_special_tokens=True)
        inputs = self.processor(
            audios, sampling_rate=SAMPLE_RATE, return_tensors="pt", padding=True
        ).to(self.device)
        inputs["input_values"] = inputs["input_values"].to(self.dtype)
        with torch.no_grad():
            logits = self.model(**inputs).logits
        return self.processor.batch_decode(logits.argmax(dim=-1))


def load_audio(path: str) -> Any:
    """Load an audio file as a 16 kHz mono float32 array."""
    import librosa

    audio, _ = librosa.load(path, sr=SAMPLE_RATE, mono=True)
    return audio
