from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class FileHash:
    path: str
    size: int
    sha256: str


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()


def scan_paths(paths: Iterable[Path]) -> list[FileHash]:
    results: list[FileHash] = []
    for p in paths:
        if p.is_file():
            results.append(FileHash(str(p), p.stat().st_size, sha256_file(p)))
        elif p.is_dir():
            for fp in sorted(p.rglob("*")):
                if fp.is_file():
                    results.append(FileHash(str(fp), fp.stat().st_size, sha256_file(fp)))
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Lyra HashScan (SHA-256) for directories/files.")
    parser.add_argument("target", help="File or directory to scan")
    parser.add_argument("--out", default="hashscan.json", help="Output JSON filename")
    args = parser.parse_args()

    target = Path(args.target).expanduser().resolve()
    if not target.exists():
        raise SystemExit(f"Target not found: {target}")

    report = scan_paths([target])
    payload = [fh.__dict__ for fh in report]
    Path(args.out).write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"OK: wrote {len(payload)} entries to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
