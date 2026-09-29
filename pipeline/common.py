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


def load_config():
    with open(ROOT / "config.json", encoding=ENCODING) as f:
        return json.load(f)


def write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding=ENCODING) as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)


def images_dir(cfg):
    """Where the committed photographs live."""
    return ROOT / cfg.get("images_dir", "images")
