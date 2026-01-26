from pathlib import Path
from lyra_python.tools.hashscan import sha256_file


def test_sha256_file(tmp_path: Path):
    p = tmp_path / "a.txt"
    p.write_text("lyra", encoding="utf-8")
    h = sha256_file(p)
    assert isinstance(h, str)
    assert len(h) == 64
