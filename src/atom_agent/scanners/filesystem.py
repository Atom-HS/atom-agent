"""Filesystem scanner — scan local folders, produce ScanResults."""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from atom_agent.config import IGNORE_FILES
from atom_agent.core.hasher import hash_file
from atom_agent.core.classifier import classify
from atom_agent.core.namer import generate_name, generate_destination
from atom_agent.core.dedup import is_duplicate
import mimetypes


@dataclass
class ScanResult:
    original_path: str
    file_hash: str
    mime: str
    size: int
    file_date: datetime
    proposed_title: str
    proposed_type: str
    proposed_module: str
    proposed_tags: list[str]
    proposed_destination: str
    proposed_filename: str
    action: str  # move | trash | duplicate | skip | manual
    confidence: float
    reasoning: str
    duplicate_of: str | None = None


def scan_folder(source: Path, deep: bool = False) -> list[ScanResult]:
    if not source.exists():
        raise FileNotFoundError(f"Source folder does not exist: {source}")
    if not source.is_dir():
        raise NotADirectoryError(f"Not a directory: {source}")

    results: list[ScanResult] = []
    pattern = "**/*" if deep else "*"

    for path in sorted(source.glob(pattern)):
        if not path.is_file() or path.name in IGNORE_FILES:
            continue

        file_hash = hash_file(path)
        is_dup, dup_id = is_duplicate(file_hash)

        if is_dup:
            results.append(ScanResult(
                original_path=str(path), file_hash=file_hash, mime=_guess_mime(path.suffix),
                size=path.stat().st_size, file_date=datetime.fromtimestamp(path.stat().st_mtime),
                proposed_title=path.name, proposed_type="", proposed_module="",
                proposed_tags=[], proposed_destination="lixo/duplicatas/", proposed_filename=path.name,
                action="duplicate", confidence=1.0, reasoning="hash match", duplicate_of=dup_id,
            ))
            continue

        classification = classify(path)

        if classification.is_trash:
            results.append(ScanResult(
                original_path=str(path), file_hash=file_hash, mime=_guess_mime(path.suffix),
                size=path.stat().st_size, file_date=datetime.fromtimestamp(path.stat().st_mtime),
                proposed_title=path.name, proposed_type="trash", proposed_module="",
                proposed_tags=[], proposed_destination="lixo/trash/", proposed_filename=path.name,
                action="trash", confidence=classification.confidence, reasoning=classification.reasoning,
            ))
            continue

        file_date = datetime.fromtimestamp(path.stat().st_mtime)
        new_name = generate_name(path, classification, file_date)
        dest = generate_destination(classification)
        action = "manual" if classification.confidence < 0.5 else "move"

        results.append(ScanResult(
            original_path=str(path), file_hash=file_hash, mime=_guess_mime(path.suffix),
            size=path.stat().st_size, file_date=file_date,
            proposed_title=path.name, proposed_type=classification.atom_type,
            proposed_module=classification.module, proposed_tags=classification.tags,
            proposed_destination=dest, proposed_filename=new_name,
            action=action, confidence=classification.confidence, reasoning=classification.reasoning,
        ))

    return results


def _guess_mime(ext: str) -> str:
    mime, _ = mimetypes.guess_type(f"file{ext}")
    return mime or "application/octet-stream"
