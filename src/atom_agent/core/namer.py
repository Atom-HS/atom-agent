"""Naming convention — Genesis 8.4 applied to filenames."""

from __future__ import annotations
import re
from datetime import datetime
from pathlib import Path
from atom_agent.core.classifier import Classification


def generate_name(path: Path, classification: Classification, file_date: datetime | None = None) -> str:
    ext = path.suffix.lower()
    mod = classification.module
    if classification.is_trash or not mod:
        return path.name

    desc = path.stem
    desc = re.sub(r"[^a-zA-Z0-9\s\-]", "", desc)
    desc = re.sub(r"\s+", "-", desc.strip()).lower()
    desc = re.sub(r"-+", "-", desc)[:50].rstrip("-")

    if file_date is None:
        file_date = datetime.fromtimestamp(path.stat().st_mtime)
    date_str = file_date.strftime("%Y-%m-%d")

    return f"mod-{mod}_{classification.atom_type}_{desc}_{date_str}{ext}"


def generate_destination(classification: Classification) -> str:
    if classification.is_trash:
        return "lixo/trash/"
    if "#vital-doc" in classification.tags:
        return "mod-bridge/documents/"
    mod = classification.module
    return f"mod-{mod}/" if mod else "inbox/"
