import tempfile
from pathlib import Path
from atom_agent.core.hasher import hash_file


def test_hash_known_content():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as f:
        f.write(b"hello atom agent")
        f.flush()
        h = hash_file(Path(f.name))
    assert len(h) == 64
    assert h == hash_file(Path(f.name))


def test_hash_empty_file():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.flush()
        h = hash_file(Path(f.name))
    assert h == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"


def test_hash_different_content():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as f1:
        f1.write(b"file A")
        f1.flush()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as f2:
        f2.write(b"file B")
        f2.flush()
    assert hash_file(Path(f1.name)) != hash_file(Path(f2.name))
