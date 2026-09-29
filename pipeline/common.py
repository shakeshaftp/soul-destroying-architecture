"""Shared helpers. Nothing here usually needs changing."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SITE = ROOT / "site"
TEMPLATES = ROOT / "templates"

# Every read and write in this pipeline is explicitly UTF-8. Without this,
# Python on Windows falls back to the system code page and the pipeline dies
# on the first accented name — Säynätsalo, Poundbury's café, an em dash.
# GitHub Actions runs on Linux and would not have shown you the problem.
ENCODING = "utf-8"

# Line ending for everything this pipeline writes. Pinned so that a run on a
# Windows laptop and a run on the Linux CI runner produce identical bytes.
NEWLINE = "\n"


def load_config():
    with open(ROOT / "config.json", encoding=ENCODING) as f:
        return json.load(f)


def write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    # NEWLINE stops Windows translating to CRLF. The daily job compares this
    # file against the committed one byte for byte, so the two platforms have
    # to agree on line endings.
    with open(path, "w", encoding=ENCODING, newline=NEWLINE) as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)


def images_dir(cfg):
    """Where the committed photographs live."""
    return ROOT / cfg.get("images_dir", "images")
