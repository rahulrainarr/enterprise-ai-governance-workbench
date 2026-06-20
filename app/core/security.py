from __future__ import annotations

from pathlib import Path


BLOCKED_PATH_TOKENS = (
    "05chatgpt",
    "browser export",
    "email export",
    "credentials",
    ".env",
    "vectorstore",
    "chroma",
    "faiss",
    "uploads",
    "logs",
    "installer",
    "ollama",
    "nodejs",
    "chatbox",
    "node_modules",
    ".venv",
    "__pycache__",
)

BLOCKED_SUFFIXES = {".db", ".sqlite", ".sqlite3", ".log", ".bak", ".zip", ".7z", ".onnx", ".gguf", ".env"}


def is_blocked_path(path: str | Path) -> bool:
    text = str(path).replace("\\", "/").lower()
    if any(token in text for token in BLOCKED_PATH_TOKENS):
        return True
    return Path(path).suffix.lower() in BLOCKED_SUFFIXES


def ensure_ingestion_allowed(path: str | Path) -> Path:
    candidate = Path(path)
    if is_blocked_path(candidate):
        raise ValueError(f"Blocked by local data policy: {candidate}")
    return candidate
