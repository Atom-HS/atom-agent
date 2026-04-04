"""Physical file mover — move + verify hash + integrity check."""

from __future__ import annotations
import shutil
from pathlib import Path
from atom_agent.core.hasher import hash_file


class MoveError(Exception):
    pass


def move_file(source: Path, destination: Path, expected_hash: str) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        stem, ext, counter = destination.stem, destination.suffix, 1
        while destination.exists():
            destination = destination.parent / f"{stem}_{counter}{ext}"
            counter += 1

    shutil.move(str(source), str(destination))

    post_hash = hash_file(destination)
    if post_hash != expected_hash:
        shutil.move(str(destination), str(source))
        raise MoveError(f"Hash mismatch: expected {expected_hash[:12]}..., got {post_hash[:12]}...")
