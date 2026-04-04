"""SHA-256 file hashing — streaming, memory-safe."""

import hashlib
from pathlib import Path

CHUNK_SIZE = 8192


def hash_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(CHUNK_SIZE), b""):
            h.update(chunk)
    return h.hexdigest()
